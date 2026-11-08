import streamlit as st
import tempfile
import urllib.request
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip

st.title("🎵 Step 3: Add Audio & Render Video")

uploaded_audio = st.file_uploader("Upload Background Audio/Voiceover (.mp3, .wav)", type=["mp3", "wav"])

if st.button("Render Final Video"):
    if "selected_video_url" not in st.session_state:
        st.error("No video selected. Please go back to Step 1.")
    else:
        try:
            # Step 1: Download raw video to temporary file
            with st.spinner("Downloading raw clip..."):
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                urllib.request.urlretrieve(st.session_state["selected_video_url"], tfile.name)
                
            # Step 2: Process video with MoviePy
            with st.spinner("Editing video and combining audio..."):
                clip = VideoFileClip(tfile.name)
                
                final_video = clip
                
                # Apply audio if uploaded
                if uploaded_audio is not None:
                    audio_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    audio_tmp.write(uploaded_audio.read())
                    audio_clip = AudioFileClip(audio_tmp.name).set_duration(clip.duration)
                    final_video = final_video.set_audio(audio_clip)
                    
                out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                final_video.write_videofile(out_file, codec="libx264", audio_codec="aac", fps=24)
                
                st.session_state["rendered_video_path"] = out_file
                st.success("Rendering complete! Proceed to Step 4.")
        except Exception as e:
            st.error(f"An error occurred during rendering: {e}")
