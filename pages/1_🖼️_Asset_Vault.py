import streamlit as st
import tempfile
import os

st.title("🖼️ Step 1: Asset Vault & Uploads")
st.caption("Upload your custom visuals, character cutouts, backgrounds, and audio files.")

if "assets" not in st.session_state:
    st.session_state["assets"] = {"images": [], "cartoons": [], "backgrounds": [], "audio": []}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Visual Assets")
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
    st.subheader("Audio & Music Assets")
    uploaded_voiceover = st.file_uploader("Upload Voiceover Audio (.mp3, .wav)", type=["mp3", "wav"])
    uploaded_bgm = st.file_uploader("Upload Background Music Track (.mp3, .wav)", type=["mp3", "wav"])

if st.button("Process & Save Assets"):
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

    st.success(f"Assets loaded! {len(assets['images'])} background images and {len(assets['cartoons'])} overlays stored.")

st.markdown("---")
st.write("### Current Vault Inventory")
st.write(f"- **Scene Images:** {len(st.session_state['assets']['images'])}")
st.write(f"- **Cartoon Overlays:** {len(st.session_state['assets']['cartoons'])}")
st.write(f"- **Audio Tracks:** {len(st.session_state['assets']['audio'])}")
