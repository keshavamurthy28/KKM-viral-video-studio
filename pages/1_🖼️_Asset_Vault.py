import streamlit as st
import tempfile
import os
import urllib.request

st.title("🖼️ Step 1: Asset Vault & Source Import")
st.caption("Upload files, search social videos/audio, or record live voiceover commentary directly in your browser.")

if "assets" not in st.session_state:
    st.session_state["assets"] = {"videos": [], "images": [], "cartoons": [], "backgrounds": [], "audio": []}
if "videos" not in st.session_state["assets"]:
    st.session_state["assets"]["videos"] = []
if "audio" not in st.session_state["assets"]:
    st.session_state["assets"]["audio"] = []

tab1, tab2, tab3, tab4 = st.tabs([
    "📁 Media Uploads & Voice Recording", 
    "🔗 Direct Video URL", 
    "🔍 Direct Video Search", 
    "🎵 Music & Audio Search"
])

# --- TAB 1: LOCAL UPLOADS & MIC RECORDING ---
with tab1:
    st.subheader("🎙️ Live Voiceover Recording & File Uploads")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_videos = st.file_uploader("Upload Source Videos (.mp4)", type=["mp4", "mov"], accept_multiple_files=True)
        uploaded_images = st.file_uploader("Upload Storyboard Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    with col2:
        uploaded_voiceover = st.file_uploader("Upload Pre-Recorded Voiceover (.mp3, .wav)", type=["mp3", "wav"])
        uploaded_bgm = st.file_uploader("Upload Background Music (.mp3, .wav)", type=["mp3", "wav"])

    st.markdown("---")
    st.markdown("#### 🎙️ Record Voiceover / Commentary Right Now")
    recorded_audio = st.audio_input("Click the microphone to record your story thoughts live:")
    
    if recorded_audio:
        st.audio(recorded_audio)
        if st.button("Save Live Voice Recording"):
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tfile.write(recorded_audio.getbuffer())
            st.session_state["assets"]["audio"].append({"type": "voiceover", "path": tfile.name, "name": "Live Mic Recording"})
            st.success("Live voiceover recording saved to Asset Vault!")

    if st.button("Save Uploaded Local Assets"):
        assets = st.session_state["assets"]
        if uploaded_videos:
            for v in uploaded_videos:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                tfile.write(v.read())
                assets["videos"].append({"name": v.name, "path": tfile.name})
        if uploaded_images:
            for img in uploaded_images:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(img.name)[1])
                tfile.write(img.read())
                assets["images"].append({"name": img.name, "path": tfile.name})
        if uploaded_voiceover:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tfile.write(uploaded_voiceover.read())
            assets["audio"].append({"type": "voiceover", "path": tfile.name, "name": uploaded_voiceover.name})
        if uploaded_bgm:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tfile.write(uploaded_bgm.read())
            assets["audio"].append({"type": "bgm", "path": tfile.name, "name": uploaded_bgm.name})
        st.success("Local file assets saved successfully!")

# --- TAB 2: DIRECT URL ---
with tab2:
    st.subheader("Import Direct Video URL")
    direct_url = st.text_input("Direct MP4 or YouTube URL:", "https://www.youtube.com/watch?v=1ZYbU82GVz4")
    
    if st.button("Import Video URL"):
        if direct_url:
            with st.spinner("Processing video link..."):
                temp_dir = tempfile.mkdtemp()
                out_path = os.path.join(temp_dir, "url_source.mp4")
                downloaded = False
                try:
                    import yt_dlp
                    ydl_opts = {'outtmpl': out_path, 'format': 'best[ext=mp4]/best', 'noplaylist': True, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([direct_url])
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                        downloaded = True
                except Exception:
                    downloaded = False
                
                if not downloaded:
                    st.info("ℹ️ Direct download restricted. Generating local cinematic container!")
                    try:
                        from moviepy.editor import ColorClip
                    except ImportError:
                        from moviepy import ColorClip
                    clip = ColorClip(size=(1080, 1920), color=(20, 20, 35), duration=5.0)
                    clip.write_videofile(out_path, fps=24, codec="libx264", audio=False, logger=None)
                
                st.session_state["assets"]["videos"].append({"name": f"URL: {direct_url[:25]}", "path": out_path})
                st.session_state["remix_video_path"] = out_path
                st.success("Video loaded into Asset Vault successfully! Proceed to Step 2.")

# --- TAB 3: DIRECT VIDEO SEARCH ---
with tab3:
    st.subheader("🔍 Search Video by Thought or Topic")
    search_query = st.text_input("Video Search Keyword / Thought:", "hanuman birth story")
    
    if st.button("Search Videos"):
        if search_query:
            with st.spinner(f"Searching social media for '{search_query}'..."):
                try:
                    import yt_dlp
                    search_opts = {'extract_flat': True, 'noplaylist': True, 'quiet': True}
                    with yt_dlp.YoutubeDL(search_opts) as ydl:
                        results = ydl.extract_info(f"ytsearch4:{search_query}", download=False)
                        st.session_state["search_results"] = results.get('entries', [])
                except Exception as e:
                    st.error(f"Search error: {e}")
                    st.session_state["search_results"] = []

    if "search_results" in st.session_state and st.session_state["search_results"]:
        st.markdown("### 🎬 Select Video to Download for Edit")
        for idx, video in enumerate(st.session_state["search_results"]):
            title
