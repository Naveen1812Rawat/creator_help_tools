from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import re
import os
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Downloader API"}

@app.get("/download/")
def download_video(url: str):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path="downloads", filename="video.mp4")
        return FileResponse(os.path.join("downloads", "video.mp4"), filename="video.mp4")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1819)
