from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import re
import os
from urllib.parse import parse_qs, urlparse

def extract_video_id(url: str) -> str:
    # Extract the video ID from the URL
    video_info = []
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        print(parsed_url.path)
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        if parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        if parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    
    return None