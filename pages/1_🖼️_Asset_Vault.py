import streamlit as st
import tempfile
import os

st.title("🖼️ Step 1: Asset Vault & Video Source")
st.caption("Upload your local assets or provide a direct public MP4 video link.")

if "assets" not in st.session_state:
    st.session_state["assets"] = {"images": [], "cartoons": [], "backgrounds": [], "audio": []}
if "social_edit_config" not in st.session_state:
    st.session_state["social_edit_config"] = None

tab1, tab2 = st.tabs(["📁 Custom Asset Uploads", "🔗 Direct Video URL (MP4)"])

with tab1:
    st.subheader("Upload Scene Backgrounds & Audio")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        uploaded_cartoons = st.file_uploader("Upload Transparent Cutouts", type=["png"], accept_multiple_files=True)

    with col2:
        uploaded_voiceover = st.file_uploader("Upload Voiceover (.mp3, .wav)", type=["mp3", "wav"])
        uploaded_bgm = st.file_uploader("Upload Background Music (.mp3, .wav)", type=["mp3", "wav"])

    if st.button("Save Assets"):
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
        st.success("Assets saved successfully!")

with tab2:
    st.subheader("Paste Direct MP4 Video URL")
    st.markdown("Paste any direct public `.mp4` video link (e.g., from free stock video sites like Pexels or Pixabay):")
    direct_url = st.text_input("Direct Video URL:", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
    
    if st.button("Load Video URL"):
        if direct_url:
            st.session_state["social_edit_config"] = {"video_url": direct_url}
            st.session_state["storyboard_mode"] = "social"
            st.success("Direct video loaded successfully! Proceed to Step 3.")
