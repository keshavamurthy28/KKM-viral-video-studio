import streamlit as st
import tempfile
import numpy as np
import os
from PIL import Image, ImageDraw

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

creation_mode = st.session_state.get("creation_mode", "🔄 Remix Social Video with Thoughts")
remix_config = st.session_state.get("remix_config", {})
remix_video_path = st.session_state.get("remix_video_path", None)
storyboard = st.session_state.get("storyboard", [])
assets = st.session_state.get("assets", {"audio": []})

bgm_volume = st.slider("Background Music Volume", 0.0, 1.0, 0.2)
voice_volume = st.slider("Voiceover Volume", 0.0, 2.0, 1.0)
target_size = (1080, 1920)

if st.button("🚀 Render Final Viral Video"):
    try:
        with st.spinner("Processing video frames, burning text thoughts, and mixing audio tracks..."):
            final_video = None
            
            if creation_mode == "🔄 Remix Social Video with Thoughts" and remix_video_path:
                clip = VideoFileClip(remix_video_path)
                max_dur = min(clip.duration, remix_config.get("duration", 15))
                
                if hasattr(clip, "subclipped"):
                    clip = clip.subclipped(0, max_dur)
                elif hasattr(clip, "subclip"):
                    clip = clip.subclip(0, max_dur)
                    
                if hasattr(clip, "resized"):
                    clip = clip.resized(target_size)
                elif hasattr(clip, "resize"):
                    clip = clip.resize(target_size)
                
                top_text = remix_config.get("top_hook", "")
                bottom_text = remix_config.get("bottom_thought", "")
                
                def add_captions(get_frame, t):
                    frame = get_frame(t)
                    img = Image.fromarray(frame)
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(50, 100), (1030, 240)], fill=(0, 0, 0, 200))
                    draw.text((70, 120), top_text, fill=(255, 255, 255))
                    draw.rectangle([(50, 1500), (1030, 1800)], fill=(0, 0, 0, 200))
                    draw.text((70, 1530), bottom_text, fill=(255, 255, 255))
                    return np.array(img)
                
                final_video = clip.fl(add_captions)
            else:
                rendered_scene_clips = []
                for scene in storyboard:
                    raw_img = Image.open(scene["image_path"]).convert("RGB")
                    raw_img = raw_img.resize(target_size, Image.Resampling.LANCZOS)
                    img_np = np.array(raw_img)
                    base_clip = ImageClip(img_np).set_duration(scene["duration"])
                    duration = scene["duration"]
                    
                    if scene["motion"] == "Zoom In (Ken Burns)":
                        if hasattr(base_clip, "resized"):
                            base_clip = base_clip.resized(lambda t: 1.0 + 0.08 * (t / duration))
                        else:
                            base_clip = base_clip.resize(lambda t: 1.0 + 0.08 * (t / duration))
                    elif scene["motion"] == "Pan Left to Right":
                        base_clip = base_clip.set_position(lambda t: (int(-50 + 50 * (t / duration)), "center"))

                    scene_composite = CompositeVideoClip([base_clip], size=target_size).set_duration(duration)
                    rendered_scene_clips.append(scene_composite)

                final_video = concatenate_videoclips(rendered_scene_clips, method="compose")

            audio_tracks = []
            for a in assets.get("audio", []):
                if a.get("path") and os.path.exists(a["path"]):
                    if a["type"] == "voiceover":
                        voice_clip = AudioFileClip(a["path"]).volumex(voice_volume)
                        audio_tracks.append(voice_clip)
                    elif a["type"] == "bgm":
                        bgm_clip = AudioFileClip(a["path"]).volumex(bgm_volume)
                        if bgm_clip.duration < final_video.duration:
                            bgm_clip = bgm_clip.loop(duration=final_video.duration)
                        else:
                            bgm_clip = bgm_clip.set_duration(final_video.duration)
                        audio_tracks.append(bgm_clip)

            if audio_tracks:
                final_audio = CompositeAudioClip(audio_tracks).set_duration(final_video.duration)
                final_video = final_video.set_audio(final_audio)

            out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            final_video.write_videofile(
                out_file, 
                fps=24, 
                codec="libx264", 
                audio_codec="aac",
                threads=2,
                preset="ultrafast"
            )
            
            st.session_state["rendered_video_path"] = out_file
            st.success("🎉 Video rendered successfully with your thoughts and audio tracks! Proceed to Step 4.")
            
    except Exception as e:
        st.error(f"Render Error: {e}")
