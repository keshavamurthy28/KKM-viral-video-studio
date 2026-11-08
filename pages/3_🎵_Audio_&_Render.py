import streamlit as st
import tempfile
import numpy as np
from PIL import Image

try:
    from moviepy.editor import (
        ImageClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips
    )
except ImportError:
    from moviepy import (
        ImageClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips
    )

st.title("🎵 Step 3: Multi-Track Audio & High-End Render Engine")

storyboard = st.session_state.get("storyboard", [])
assets = st.session_state.get("assets", {"audio": []})

if not storyboard:
    st.warning("No storyboard configured. Please complete Step 2 first.")
else:
    st.subheader("Audio Settings")
    bgm_volume = st.slider("Background Music Volume", 0.0, 1.0, 0.2)
    voice_volume = st.slider("Voiceover Volume", 0.0, 2.0, 1.0)
    
    output_resolution = st.selectbox("Render Format Ratio", ["9:16 Vertical Short (1080x1920)", "16:9 Landscape (1920x1080)"])
    target_size = (1080, 1920) if "9:16" in output_resolution else (1920, 1080)

    if st.button("🚀 Render Final Animation Video"):
        try:
            with st.spinner("Processing motion animations, layering character overlays, and rendering..."):
                rendered_scene_clips = []
                
                for scene in storyboard:
                    # 1. Base Image Setup & Resize to Target Canvas
                    raw_img = Image.open(scene["image_path"]).convert("RGB")
                    raw_img = raw_img.resize(target_size, Image.Resampling.LANCZOS)
                    img_np = np.array(raw_img)
                    
                    base_clip = ImageClip(img_np).set_duration(scene["duration"])
                    
                    # 2. Advanced Motion Animation (Ken Burns Zoom/Pan Effects)
                    duration = scene["duration"]
                    if scene["motion"] == "Zoom In (Ken Burns)":
                        base_clip = base_clip.resize(lambda t: 1.0 + 0.08 * (t / duration))
                    elif scene["motion"] == "Pan Left to Right":
                        base_clip = base_clip.set_position(lambda t: (int(-50 + 50 * (t / duration)), "center"))
                    elif scene["motion"] == "Pan Right to Left":
                        base_clip = base_clip.set_position(lambda t: (int(0 - 50 * (t / duration)), "center"))

                    layers = [base_clip]
                    
                    # 3. Apply Character/Cartoon Cutout Overlay
                    if scene["cartoon_path"]:
                        cartoon_img = Image.open(scene["cartoon_path"]).convert("RGBA")
                        c_width = int(target_size[0] * 0.4)
                        c_height = int(cartoon_img.height * (c_width / cartoon_img.width))
                        cartoon_img = cartoon_img.resize((c_width, c_height), Image.Resampling.LANCZOS)
                        
                        cartoon_clip = (
                            ImageClip(np.array(cartoon_img), transparent=True)
                            .set_duration(duration)
                            .set_position(("center", "bottom"))
                        )
                        layers.append(cartoon_clip)
                        
                    scene_composite = CompositeVideoClip(layers, size=target_size).set_duration(duration)
                    rendered_scene_clips.append(scene_composite)

                # 4. Concatenate Scene Clips smoothly
                final_video = concatenate_videoclips(rendered_scene_clips, method="compose")

                # 5. Composite Multi-track Audio (BGM + Voiceover)
                audio_tracks = []
                for a in assets["audio"]:
                    if a["type"] == "voiceover":
                        voice_clip = AudioFileClip(a["path"]).volumex(voice_volume)
                        audio_tracks.append(voice_clip)
                    elif a["type"] == "bgm":
                        bgm_clip = AudioFileClip(a["path"]).volumex(bgm_volume)
                        if bgm_clip.duration < final_video.duration:
                            # Loop music if short
                            bgm_clip = bgm_clip.loop(duration=final_video.duration)
                        else:
                            bgm_clip = bgm_clip.set_duration(final_video.duration)
                        audio_tracks.append(bgm_clip)

                if audio_tracks:
                    final_audio = CompositeAudioClip(audio_tracks).set_duration(final_video.duration)
                    final_video = final_video.set_audio(final_audio)

                # 6. Render with H.264 / AAC Codecs for platform compatibility
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
                st.success("🎉 Video rendered successfully! Proceed to Step 4 to download.")
                
        except Exception as e:
            st.error(f"Render Error: {e}")
