import streamlit as st
import tempfile
import os

st.title("🖼️ Step 1: Asset Vault & Source Import")
st.caption("Upload your source videos, reference clips, voiceovers, and background music.")

if "assets" not in st.session_state:
    st.session_state["assets"] = {"videos": [], "images": [], "cartoons": [], "audio": []}

tab1, tab2 = st.tabs(["📁 Media Uploads", "🔗 Direct Video URL"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        uploaded_videos = st.file_uploader("Upload Source Videos (.mp4)", type=["mp4", "mov"], accept_multiple_files=True)
        uploaded_images = st.file_uploader("Upload Storyboard Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    with col2:
        uploaded_voiceover = st.file_uploader("Upload Voiceover/Thoughts (.mp3, .wav)", type=["mp3", "wav"])
        uploaded_bgm = st.file_uploader("Upload Background Music (.mp3, .wav)", type=["mp3", "wav"])

    if st.button("Save Vault Assets"):
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
            assets["audio"].append({"type": "voiceover", "path": tfile.name})
        if uploaded_bgm:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tfile.write(uploaded_bgm.read())
            assets["audio"].append({"type": "bgm", "path": tfile.name})
        st.success("Assets successfully saved to vault!")

with tab2:
    st.subheader("Import Public Video URL")
    direct_url = st.text_input("Direct MP4 URL:", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
    if st.button("Load URL into Vault"):
        if direct_url:
            st.session_state["assets"]["videos"].append({"name": "URL Video", "path": direct_url})
            st.success("Video URL registered successfully!")
