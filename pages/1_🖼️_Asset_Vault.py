import streamlit as st
import tempfile
import os
import yt_dlp

st.title("🖼️ Step 1: Asset Vault & Social Video Finder")
st.caption("Upload your custom visuals and audio, or search and import viral social media videos directly.")

# Initialize Session State variables
if "assets" not in st.session_state:
    st.session_state["assets"] = {"images": [], "cartoons": [], "backgrounds": [], "audio": []}
if "selected_video_url" not in st.session_state:
    st.session_state["selected_video_url"] = None

# Create tabs for clean separation of custom uploads vs. social media search
tab1, tab2 = st.tabs(["📁 Custom Asset Uploads", "🌐 Search & Import Social Videos"])

with tab1:
    st.subheader("Manage Your Local Assets")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Visual Assets**")
        uploaded_images = st.file_uploader(
            "Upload Scene Backgrounds / Main Images", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True
        )
        uploaded_cartoons = st.file_uploader(
            "Upload Cartoon / Character Overlays (Transparent PNG)", 
            type=["png"], 
            accept_multiple_files=True
        )

    with col2:
        st.markdown("**Audio & Music Assets**")
        uploaded_voiceover = st.file_uploader("Upload Voiceover Audio (.mp3, .wav)", type=["mp3", "wav"])
        uploaded_bgm = st.file_uploader("Upload Background Music Track (.mp3, .wav)", type=["mp3", "wav"])

    if st.button("Save Custom Assets"):
        assets = st.session_state["assets"]
        
        if uploaded_images:
            for img in uploaded_images:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(img.name)[1])
                tfile.write(img.read())
                assets["images"].append({"name": img.name, "path": tfile.name})
                
        if uploaded_cartoons:
            for c in uploaded_cartoons:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                tfile.write(c.read())
                assets["cartoons"].append({"name": c.name, "path": tfile.name})
                
        if uploaded_voiceover:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tfile.write(uploaded_voiceover.read())
            assets["audio"].append({"type": "voiceover", "path": tfile.name})

        if uploaded_bgm:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tfile.write(uploaded_bgm.read())
            assets["audio"].append({"type": "bgm", "path": tfile.name})

        st.success("Custom assets saved successfully!")

with tab2:
    st.subheader("Find & Import Content from Social Media")
    search_query = st.text_input("Type topic/keyword to search trending social videos (e.g., 'mythology storytelling facts'):", "viral shorts")

    if st.button("Search Social Platforms"):
        with st.spinner("Searching social media feeds..."):
            ydl_opts = {
                'extract_flat': True,
                'max_results': 5,
                'default_search': 'ytsearch5'
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch5:{search_query}", download=False)
                    if 'entries' in info:
                        st.session_state["social_search_results"] = info['entries']
            except Exception as e:
                st.error(f"Error fetching social content: {e}")

    if "social_search_results" in st.session_state:
        st.markdown("### Search Results (Click 'Import' to select)")
        for idx, item in enumerate(st.session_state["social_search_results"]):
            title = item.get('title', 'Untitled Video')
            vid_id = item.get('id', '')
            vid_url = f"https://www.youtube.com/watch?v={vid_id}"
            
            cols = st.columns([3, 1])
            with cols[0]:
                st.write(f"**{title}**")
                st.video(vid_url)
            with cols[1]:
                if st.button("Import Video", key=f"import_vid_{idx}"):
                    st.session_state["selected_video_url"] = vid_url
                    st.success("Imported! Ready for alterations.")

    if st.session_state["selected_video_url"]:
        st.info(f"Currently active imported social video URL: `{st.session_state['selected_video_url']}`")

st.markdown("---")
st.markdown("### Vault Summary")
st.write(f"- **Local Scene Images:** {len(st.session_state['assets']['images'])}")
st.write(f"- **Cartoon/Character Overlays:** {len(st.session_state['assets']['cartoons'])}")
st.write(f"- **Imported Social Video URL:** {'Loaded & Ready' if st.session_state['selected_video_url'] else 'None'}")
