import streamlit as st
import requests

st.title("🔍 Step 1: Find Viral Video Footage")

query = st.text_input("Search Pexels Stock Video (e.g., 'nature cinematic', 'cyberpunk city'):", "nature")
pexels_api_key = st.text_input("Pexels API Key (Free from pexels.com/api):", type="password")

if st.button("Search Videos"):
    if not pexels_api_key:
        st.error("Please enter a free Pexels API key.")
    else:
        headers = {"Authorization": pexels_api_key}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=portrait"
        res = requests.get(url, headers=headers).json()
        
        if "videos" in res:
            st.session_state["search_results"] = res["videos"]

if "search_results" in st.session_state:
    for vid in st.session_state["search_results"]:
        st.video(vid["video_files"][0]["link"])
        if st.button(f"Select Video ID #{vid['id']}", key=vid["id"]):
            st.session_state["selected_video_url"] = vid["video_files"][0]["link"]
            st.success("Selected! Proceed to Step 2 in the sidebar.")
