import streamlit as st

st.title("📜 Step 2: Storyboard & Animation Engine")
st.caption("Assemble your scenes, apply Ken Burns smooth motion animations, and set timed story captions.")

assets = st.session_state.get("assets", {"images": [], "cartoons": []})

if not assets["images"]:
    st.warning("No scene images found in Asset Vault. Please upload visuals in Step 1.")
else:
    st.subheader("Scene Sequence Configuration")
    scene_count = st.number_input("Number of Story Scenes:", min_value=1, max_value=10, value=len(assets["images"]))
    
    storyboard = []
    
    for i in range(int(scene_count)):
        st.markdown(f"#### Scene {i+1}")
        col_img, col_cfg = st.columns([1, 2])
        
        with col_img:
            img_names = [img["name"] for img in assets["images"]]
            selected_img_name = st.selectbox(f"Select Visual for Scene {i+1}", img_names, key=f"img_{i}")
            selected_img_path = next(img["path"] for img in assets["images"] if img["name"] == selected_img_name)
            st.image(selected_img_path, width=150)
            
        with col_cfg:
            duration = st.slider(f"Scene {i+1} Duration (seconds)", 1.0, 10.0, 3.0, key=f"dur_{i}")
            caption = st.text_input(f"Subtitle / Story Text for Scene {i+1}", f"Story Caption for scene {i+1}", key=f"txt_{i}")
            motion = st.selectbox(
                f"Camera Motion Effect (Animation)", 
                ["Zoom In (Ken Burns)", "Pan Left to Right", "Pan Right to Left", "Static Focus"], 
                key=f"mot_{i}"
            )
            
            cartoon_names = ["None"] + [c["name"] for c in assets["cartoons"]]
            selected_cartoon = st.selectbox(f"Character Overlay for Scene {i+1}", cartoon_names, key=f"cart_{i}")
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
        
    if st.button("Save Storyboard Settings"):
        st.session_state["storyboard"] = storyboard
        st.success("Storyboard built successfully! Move to Step 3 for Audio & Rendering.")
