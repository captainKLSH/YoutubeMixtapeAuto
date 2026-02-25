import streamlit as st
import requests

st.set_page_config(page_title="AI Mixtape Generator", layout="centered")

# --- MEMORY INITIALIZATION ---
# This keeps the data alive even when buttons are clicked
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

st.title("🎵 YouTube Mixtape Automator")

# Inputs
vidname = st.text_input("Enter Video Name", placeholder="e.g., Summer_LoFi_2026")
bg_image = st.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"])
audio_files = st.file_uploader("Upload Songs", type=["mp3", "wav"], accept_multiple_files=True)

# Generate Button
if st.button("🚀 Generate Mixtape"):
    if bg_image and audio_files and vidname:
        clean_name = vidname.replace(" ", "_")
        with st.spinner("Processing... please wait."):
            
            files = [('bg_image', (bg_image.name, bg_image.getvalue(), bg_image.type))]
            for audio in audio_files:
                files.append(('songs', (audio.name, audio.getvalue(), audio.type)))
            
            data = {'project_name': clean_name}
            
            try:
                response = requests.post("http://localhost:8000/process", files=files, data=data)
                if response.status_code == 200:
                    # Store everything in memory so it doesn't disappear
                    st.session_state.processed_data = response.json()
                    st.session_state.current_vidname = clean_name
                else:
                    st.error("Backend Error: Check your terminal.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.warning("Please fill in all fields.")

# --- PERSISTENT DISPLAY AREA ---
# This section only shows up if there is data in the "Memory"
if st.session_state.processed_data:
    res = st.session_state.processed_data
    save_name = st.session_state.current_vidname

    st.divider()
    st.success(f"✅ Result for: {save_name}")

    # Description Box
    st.text_area("YouTube Description:", res['description'], height=250)
    
    # Video Preview
    video_url = f"http://localhost:8000/download/{res['video_file']}"
    st.video(video_url)

    # Download Section
    st.write("### ⬇️ Save Files")
    col1, col2 = st.columns(2)
    
    with col1:
        # We fetch the content once
        mp3_content = requests.get(f"http://localhost:8000/download/{res['audio_file']}").content
        st.download_button("Download MP3", data=mp3_content, file_name=f"{save_name}.mp3")

    with col2:
        mp4_content = requests.get(video_url).content
        st.download_button("Download MP4", data=mp4_content, file_name=f"{save_name}.mp4")

    # Reset Button (Optional: Only refresh when you say so)
    if st.button("🗑️ Clear and Start New Project"):
        st.session_state.processed_data = None
        st.rerun()