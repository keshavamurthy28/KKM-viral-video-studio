import streamlit as st

st.title("🎞️ Step 2: Remix & Storyboard Studio")
st.caption("Configure your commentary thoughts or custom storyboard scenes.")

assets = st.session_state.get("assets", {"videos": [], "images": []})

mode = st.radio("Select Creation Mode:", ["🔄 Remix Social Video with Thoughts", "🎨 Custom Image Storyboard"])
st.session_state["creation_mode"] = mode

if mode == "🔄 Remix Social Video with Thoughts":
    st.subheader("Social Video Commentary & Thought Overlays")
    
    video_list = assets.get("videos", [])
    if not video_list:
        st.warning("⚠️ No videos found in Vault. Please import a video URL or upload one in Step 1.")
    else:
        video_names = [v["name"] for v in video_list]
        selected_name = st.selectbox("Select Source Video from Vault", video_names)
        selected_vid = next(v for v in video_list if v["name"] == selected_name)
        st.session_state["remix_video_path"] = selected_vid["path"]
        
        st.video(selected_vid["path"])
        
        st.markdown("### 💬 Your Thoughts & Commentary Script")
        top_hook = st.text_input("Top Retention Hook (Headline)", "Wait until you see this part... 🤯")
        bottom_thought = st.text_area("Your Core Thoughts / Commentary Script", "Here is my perspective on why this changes everything...")
        trim_duration = st.slider("Clip Trim Duration (Seconds)", 3, 60, 15)
        
        st.session_state["remix_config"] = {
            "top_hook": top_hook,
            "bottom_thought": bottom_thought,
            "duration": trim_duration
        }
        
        if st.button("Save Remix Configuration"):
            st.success("Remix configuration saved! Proceed to Step 3.")

else:
    st.subheader("Custom Image Storyboard Builder")
    images_list = assets.get("images", [])
    if not images_list:
        st.warning("⚠️ Please upload background images in Step 1 first.")
    else:
        storyboard = []
        for i, img in enumerate(images_list):
            with st.expander(f"Scene {i+1}: {img['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    duration = st.slider(f"Duration (s) {i}", 2, 10, 4, key=f"dur_{i}")
                    motion = st.selectbox(f"Motion Effect {i}", ["Zoom In (Ken Burns)", "Pan Left to Right", "Static"], key=f"mot_{i}")
                with col2:
                    caption = st.text_input(f"Scene Text / Thought {i}", key=f"cap_{i}")
                storyboard.append({
                    "image_path": img["path"],
                    "duration": duration,
                    "motion": motion,
                    "caption": caption
                })
        st.session_state["storyboard"] = storyboard
        if st.button("Save Storyboard"):
            st.success("Storyboard saved successfully! Proceed to Step 3.")
