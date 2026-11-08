import streamlit as st
import tempfile
import numpy as np
import urllib.request
from PIL import Image

try:
    from moviepy.editor import (
        ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips
    )
except ImportError:
    from moviepy import (
        ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips
    )

st.title("🎵 Step 3: Multi-Track Audio & High-End Render Engine")

storyboard_mode = st.session_state.get("storyboard_mode", None)
storyboard = st.session_state.get("storyboard", [])
social_config = st.session_state.get("social_edit_config", None)
assets = st.session_state.get("assets", {"audio": []})

if not storyboard_mode:
    st.warning("⚠️ No configuration found. Please complete **Step 2: Storyboard & Animation** first and click save.")
else:
    st.subheader("Audio Settings")
    bgm_volume = st.slider("Background Music Volume", 0.0, 1.0, 0.2)
    voice_volume = st.slider("Voiceover Volume", 0.0, 2.0, 1.0)
    
    output_resolution = st.selectbox("Render Format Ratio", ["9:16 Vertical Short (1080x1920)", "16:9 Landscape (1920x1080)"])
    target_size = (1080, 1920) if "9:16" in output_resolution else (1920, 1080)

    if st.button("🚀 Render Final Video"):
        try:
            with st.spinner("Processing video, applying edits, and rendering..."):
                final_video = None
                
                # --- WORKFLOW A: ALTERING SOCIAL MEDIA VIDEO ---
                if storyboard_mode == "social" and social_config:
                    video_url = social_config.get("video_url")
                    
                    import yt_dlp
                    out_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                    
                    download_success = False
                    if video_url:
                        ydl_opts = {'outtmpl': out_path, 'format': 'best', 'noplaylist': True}
                        try:
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([video_url])
                            download_success = True
                        except Exception:
                            download_success = False
                            
                    # Fallback to a guaranteed working public sample video if download fails
                    if not download_success:
                        st.info("ℹ️ YouTube link restricted. Automatically switching to a reliable sample video clip for testing!")
                        sample_url = "https://www.w3schools.com/html/mov_bbb.mp4"
                        urllib.request.urlretrieve(sample_url, out_path)
                        
                    clip = VideoFileClip(out_path)
                    clip = clip.resize(target_size)
                    final_video = clip

                # --- WORKFLOW B: CUSTOM IMAGE STORYBOARD ---
                elif storyboard_mode == "custom" and storyboard:
                    rendered_scene_clips = []
                    
                    for scene in storyboard:
                        raw_img = Image.open(scene["image_path"]).convert("RGB")
                        raw_img = raw_img.resize(target_size, Image.Resampling.LANCZOS)
                        img_np = np.array(raw_img)
                        
                        base_clip = ImageClip(img_np).set_duration(scene["duration"])
                        duration = scene["duration"]
                        
                        if scene["motion"] == "Zoom In (Ken Burns)":
                            base_clip = base_clip.resize(lambda t: 1.0 + 0.08 * (t / duration))
                        elif scene["motion"] == "Pan Left to Right":
                            base_clip = base_clip.set_position(lambda t: (int(-50 + 50 * (t / duration)), "center"))
                        elif scene["motion"] == "Pan Right to Left":
                            base_clip = base_clip.set_position(lambda t: (int(0 - 50 * (t / duration)), "center"))

                        layers = [base_clip]
                        
                        if scene["cartoon_path"]:
                            cartoon_img = Image.open(scene["cartoon_path"]).convert("RGBA")
                            c_width = int(target_size[0] * 0.4)
                            c_height = int(cartoon_img.height * (c_width / cartoon_img.width))
                            cartoon_img = cartoon_img.resize((c_width, c_height), Image.Resampling.LANCZOS)
                            
                            cartoon_clip = (
                                ImageClip(np.array(cartoon_img), transparent=True)
                                .set_duration(duration)
