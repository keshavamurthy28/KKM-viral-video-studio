import streamlit as st

st.title("✏️ Step 2: Alter & Input Overlays")

if "selected_video_url" not in st.session_state:
    st.warning("Please select a video from Step 1 first.")
else:
    st.video(st.session_state["selected_video_url"])
    
    st.subheader("Add Visual Retention Hooks")
    hook_text = st.text_input("Hook Text (e.g., '3 Secrets You Never Knew About...'):", "Top 3 Secrets Revealed")
    caption_color = st.color_picker("Text Overlay Color", "#FFFFFF")
    font_size = st.slider("Font Size", 24, 72, 48)
    
    if st.button("Save Overlay Settings"):
        st.session_state["overlay_config"] = {
            "text": hook_text,
            "color": caption_color,
            "size": font_size
        }
        st.success("Overlay saved! Proceed to Step 3.")
