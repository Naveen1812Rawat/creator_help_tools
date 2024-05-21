from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import re
import os
from urllib.parse import urlparse, parse_qs
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Downloader API"}

@app.get("/download/")
def download_video(url: str):
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        # Get streaming data
        streaming_data = fetch_streaming_data(video_id)
        print(streaming_data)
        if not streaming_data:
            raise HTTPException(status_code=400, detail="Failed to extract streaming data")

        # Get the highest resolution stream URL
        stream_url = get_highest_resolution_url(streaming_data)
        if not stream_url:
            raise HTTPException(status_code=404, detail="No suitable video stream found")

        # Download video and save to file
        output_file = download_stream(video_id, stream_url)

        return FileResponse(path=output_file, filename=f"{video_id}.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_video_id(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['youtu.be', 'www.youtube.com', 'youtube.com']:
        path_parts = parsed_url.path.split('/')
        
        if parsed_url.hostname == 'youtu.be':
            return path_parts[1]
        
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        
        if path_parts[1] in ['embed', 'v']:
            return path_parts[2]
    
    return None

def fetch_streaming_data(video_id: str) -> dict:
    video_page_url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.get(video_page_url)
    if response.status_code != 200:
        return None

    match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', response.text)
    if match:
        player_response = match.group(1)
        try:
            return json.loads(player_response).get('streamingData', {})
        except json.JSONDecodeError:
            return None

    return None

def get_highest_resolution_url(streaming_data: dict) -> str:
    if 'formats' in streaming_data:
        for format in streaming_data['formats']:
            if format.get('qualityLabel') == '720p':
                return format.get('url')
    return None

def download_stream(video_id: str, stream_url: str) -> str:
    response = requests.get(stream_url, stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download video stream")

    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{video_id}.mp4")
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=100):
            if chunk:
                f.write(chunk)
    
    return output_file

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
