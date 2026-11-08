import streamlit as st

st.title("📜 Step 2: Storyboard, Social Video & Animation Engine")
st.caption("Choose your source workflow: edit an imported social video or build a custom image storyboard with advanced motion effects.")

# Retrieve assets and selections from session state
assets = st.session_state.get("assets", {"images": [], "cartoons": []})
imported_video_url = st.session_state.get("selected_video_url", None)

# Selection mode: Social Video vs. Custom Image Storyboard
source_mode = st.radio(
    "Select Your Master Content Source:",
    ["🌐 Alter Imported Social Media Video", "🖼️ Build Custom Image Storyboard"],
    index=0 if imported_video_url else 1
)

if source_mode == "🌐 Alter Imported Social Media Video":
    st.subheader("Alter & Customize Imported Social Video")
    
    if not imported_video_url:
        st.warning("No social video imported yet. Go to **Step 1: Asset Vault** and import a video from the Social Finder tab.")
    else:
        st.success(f"Active Social Video Loaded: `{imported_video_url}`")
        st.video(imported_video_url)
        
        st.markdown("---")
        st.subheader("Edit & Overlay Configurations")
        
        social_caption = st.text_input("Main Retention Hook / Text Overlay", "Wait till the end... 🤯")
        text_color = st.color_picker("Text Overlay Color", "#FFFFFF")
        font_size = st.slider("Font Size", 24, 72, 48)
        
        # Cartoon/Character overlay selection
        cartoon_names = ["None"] + [c["name"] for c in assets.get("cartoons", [])]
        selected_cartoon = st.selectbox("Select Character / Cartoon Cutout Overlay", cartoon_names)
        cartoon_path = None
        if selected_cartoon != "None":
            cartoon_path = next(c["path"] for c in assets["cartoons"] if c["name"] == selected_cartoon)
            
        if st.button("Save Social Video Alteration Settings"):
            st.session_state["storyboard_mode"] = "social"
            st.session_state["social_edit_config"] = {
                "video_url": imported_video_url,
                "caption": social_caption,
                "color": text_color,
                "font_size": font_size,
                "cartoon_path": cartoon_path
            }
            st.success("Social video configurations saved! Proceed to Step 3 for Audio & Rendering.")

else:
    st.subheader("Custom Image Storyboard Sequence")
    
    if not assets["images"]:
        st.warning("No scene images found in Asset Vault. Please upload visuals in Step 1.")
    else:
        scene_count = st.number_input("Number of Story Scenes:", min_value=1, max_value=10, value=len(assets["images"]))
        
        storyboard = []
        for i in range(int(scene_count)):
            st.markdown(f"#### Scene {i+1}")
            col_img, col_cfg = st.columns([1, 2])
            
            with col_img:
                img_names = [img["name"] for img in assets["images"]]
                selected_img_name = st.selectbox(f"Visual for Scene {i+1}", img_names, key=f"img_{i}")
                selected_img_path = next(img["path"] for img in assets["images"] if img["name"] == selected_img_name)
                st.image(selected_img_path, width=150)
                
            with col_cfg:
                duration = st.slider(f"Duration (seconds)", 1.0, 10.0, 3.0, key=f"dur_{i}")
                caption = st.text_input(f"Subtitle Text", f"Caption {i+1}", key=f"txt_{i}")
                motion = st.selectbox(
                    f"Camera Motion Effect", 
                    ["Zoom In (Ken Burns)", "Pan Left to Right", "Pan Right to Left", "Static Focus"], 
                    key=f"mot_{i}"
                )
                
                cartoon_names = ["None"] + [c["name"] for c in assets.get("cartoons", [])]
                selected_cartoon = st.selectbox(f"Character Overlay", cartoon_names, key=f"cart_{i}")
                cartoon_path = None
                if selected_cartoon != "None":
                    cartoon_path = next(c["path"] for c in assets["cartoons"] if c["name"] == selected_cartoon)
                
            storyboard.append({
                "image_path": selected_img_path,
                "duration": duration,
                "caption": caption,
                "motion": motion,
                "cartoon_path": cartoon_path
            })
            st.markdown("---")
            
        if st.button("Save Custom Storyboard Settings"):
            st.session_state["storyboard_mode"] = "custom"
            st.session_state["storyboard"] = storyboard
            st.success("Custom storyboard built successfully! Move to Step 3.")
