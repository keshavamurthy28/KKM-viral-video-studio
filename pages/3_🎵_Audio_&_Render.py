import streamlit as st
import tempfile
import urllib.request
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

st.title("🎵 Step 3: Add Audio & Render Video")

uploaded_audio = st.file_uploader("Upload Background Audio/Voiceover (.mp3, .wav)", type=["mp3", "wav"])

if st.button("Render Final Video"):
    if "selected_video_url" not in st.session_state:
        st.error("No video selected.")
    else:

        # Step 1: Download raw video to temporary file
        with st.spinner("Downloading raw clip..."):
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            urllib.request.urlretrieve(st.session_state["selected_video_url"], tfile.name)
            
        # Step 2: Process video with MoviePy
        with st.spinner("Editing video and combining audio..."):
            clip = VideoFileClip(tfile.name)
            
            # Apply user text overlay
            cfg = st.session_state.get("overlay_config", {"text": "Viral Clip", "color": "white", "size": 40})
            txt_clip = TextClip(cfg["text"], fontsize=cfg["size"], color=cfg["color"]).set_position('center').set_duration(clip.duration)
            
            final_video = CompositeVideoClip([clip, txt_clip])
            
            # Apply audio if uploaded
            if uploaded_audio is not None:
                audio_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                audio_tmp.write(uploaded_audio.read())
                audio_clip = AudioFileClip(audio_tmp.name).set_duration(clip.duration)
                final_video = final_video.set_audio(audio_clip)
                
            out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            final_video.write_videofile(out_file, codec="libx264", fps=24)
            
            st.session_state["rendered_video_path"] = out_file
            st.success("Rendering complete! Proceed to Step 4.")
