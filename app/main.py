from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Form
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from .services import audio_service, video_service, meta_service

from .services.audio_service import process_mixtape
from .services.video_service import make_video

app = FastAPI()

@app.post("/create-mixtape/")
async def create_mixtape_endpoint(
    vidname,background_image: UploadFile = File(...),
    songs: list[UploadFile] = File(...)
):
    job_id = str(vidname)
    # 1. Save files to temp folder
    # 2. Trigger audio_service.process_mixtape
    # 3. Trigger video_service.make_video
    return {"status": "Processing", "job_id": job_id}

# Temporary folders
UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/process")
async def process_mixtape(project_name: str = Form(...),bg_image: UploadFile = File(...), songs: list[UploadFile] = File(...)):
    job_id = project_name.strip().replace(" ","_")
    job_folder = os.path.join(UPLOAD_DIR, job_id)
    if os.path.exists(job_folder):
        shutil.rmtree(job_folder)
    os.makedirs(job_folder, exist_ok=True)
    
    # Save Image
    img_path = os.path.join(job_folder, "bg.jpg")
    with open(img_path, "wb") as f:
        shutil.copyfileobj(bg_image.file, f)
        
    # Save Songs
    saved_songs = []
    for song in songs:
        path = os.path.join(job_folder, song.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(song.file, f)
        saved_songs.append(path)
        
    # 1. Generate Audio Mixtape
    audio_filename = f"{job_id}.mp3"
    audio_output = os.path.join(OUTPUT_DIR, audio_filename)
    tracklist_data = audio_service.process_mixtape(saved_songs, audio_output)
    
    # 2. Generate YouTube Metadata
    title, description = meta_service.generate_youtube_metadata(tracklist_data)
    
    # 3. Generate Video
    video_filename = f"{job_id}.mp4"
    video_output = os.path.join(OUTPUT_DIR, video_filename)
    video_service.make_video(img_path, audio_output, video_output)
    
    return {
        "audio_file": audio_filename,
        "video_file": video_filename,
        "title": title,
        "description": description
    }

@app.get("/download/{filename}")
async def download_video(filename: str):
    return FileResponse(os.path.join(OUTPUT_DIR, filename))