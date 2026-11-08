import streamlit as st

st.title("📥 Step 4: Preview & Download Final Video")

rendered_path = st.session_state.get("rendered_video_path", None)

if rendered_path:
    st.subheader("Your Masterpiece Preview")
    col_vid, col_info = st.columns([1, 1])
    
    with col_vid:
        st.video(rendered_path)
        
    with col_info:
        st.success("Production complete!")
        st.markdown("""
        **Publishing Recommendations:**
        - **YouTube Shorts & Instagram Reels:** 9:16 vertical widescreen format optimized for mobile retention.
        - **Remixed Thoughts:** Embedded with your custom headline hooks and script commentary.
        """)
        
        with open(rendered_path, "rb") as file:
            st.download_button(
                label="📥 Download High Definition MP4",
                data=file,
                file_name="kkm_viral_remix.mp4",
                mime="video/mp4"
            )
else:
    st.warning("No rendered video found. Complete Steps 1 through 3 to create your video.")
