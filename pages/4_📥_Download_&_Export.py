import streamlit as st

st.title("📥 Step 4: Preview & Download")

if "rendered_video_path" in st.session_state:
    st.video(st.session_state["rendered_video_path"])
    
    with open(st.session_state["rendered_video_path"], "rb") as file:
        st.download_button(
            label="Download Final MP4 Video",
            data=file,
            file_name="viral_content.mp4",
            mime="video/mp4"
        )
else:
    st.warning("No rendered video found. Complete steps 1-3 to generate your output.")
