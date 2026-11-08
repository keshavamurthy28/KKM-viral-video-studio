import streamlit as st
import tempfile
import os

try:
    from moviepy.editor import (
        ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips, TextClip
    )
except ImportError:
    from moviepy import (
        ImageClip, VideoFileClip, CompositeVideoClip, AudioFileClip, 
        CompositeAudioClip, concatenate_videoclips, TextClip
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
        with st.spinner("Processing video and mixing audio tracks..."):
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
                
                # Add text overlays safely using built-in composite text clips if available
                top_text = remix_config.get("top_hook", "")
                bottom_text = remix_config.get("bottom_thought", "")
                
                clips_to_composite = [clip]
                
                try:
                    if top_text:
                        txt_top = TextClip(top_text, fontsize=50, color='white', bg_color='black', size=(980, None))
                        if hasattr(txt_top, "set_duration"):
                            txt_top = txt_top.set_duration(max_dur).set_position(("center", 100))
                        clips_to_composite.append(txt_top)
                    if bottom_text:
                        txt_bot = TextClip(bottom_text, fontsize=45, color='white', bg_color='black', size=(980, None))
                        if hasattr(txt_bot, "set_duration"):
                            txt_bot = txt_bot.set_duration(max_dur).set_position(("center", 1500))
                        clips_to_composite.append(txt_bot)
                except Exception:
                    pass # Skip text clips if system lacks ImageMagick/TextClip dependencies, rendering clean video
                
                final_video = CompositeVideoClip(clips_to_composite, size=target_size)
                final_video.duration = max_dur
            else:
                rendered_scene_clips = []
                for scene in storyboard:
                    raw_img = ImageClip(scene["image_path"]).set_duration(scene["duration"])
                    if hasattr(raw_img, "resized"):
                        raw_img = raw_img.resized(target_size)
                    elif hasattr(raw_img, "resize"):
                        raw_img = raw_img.resize(target_size)
                    rendered_scene_clips.append(raw_img)

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
            st.success("🎉 Video rendered successfully! Proceed to Step 4 to download your ready-to-post video.")
            
    except Exception as e:
        st.error(f"Render Error: {e}")
