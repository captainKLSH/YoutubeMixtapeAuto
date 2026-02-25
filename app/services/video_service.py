import subprocess
import os
from PIL import Image

def make_video(image_path, audio_path, output_path, video_res=(1920, 1080), fps=1):
    """
    Converts a static image and audio file into an MP4 video.
    """
    if not os.path.exists(image_path) or not os.path.exists(audio_path):
        raise FileNotFoundError("Missing input files for video generation.")

    # Resize the image to standard YouTube HD (1920x1080)
    img_temp = "temp_resized_img.jpg"
    img = Image.open(image_path)
    img = img.resize(video_res)
    img.save(img_temp)

    # FFmpeg Command: The "Recipe" for the video
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1',          # Loop the image
        '-i', img_temp,        # Input Image
        '-i', audio_path,      # Input Audio
        '-c:v', 'libx264',     # Video Codec (High compatibility)
        '-preset', 'ultrafast',# Speed over file size
        '-tune', 'stillimage', # Optimization for static images
        '-r', str(fps),        # Frames per second (1 is enough for static)
        '-c:a', 'aac',         # Audio Codec
        '-b:a', '320k',        # High-quality audio bitrate
        '-shortest',           # Stop video when audio ends
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(img_temp):
            os.remove(img_temp)
    
    return output_path