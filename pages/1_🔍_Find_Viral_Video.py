import streamlit as st
import yt_dlp

st.title("🔍 Step 1: Fetch Live Social Content")

search_query = st.text_input("Enter Topic to Search Social Media (e.g., 'ancient history facts'):", "mythology shorts")

if st.button("Search Social Platforms"):
    with st.spinner("Searching and fetching top matching videos..."):
        ydl_opts = {
            'extract_flat': True,
            'max_results': 5,
            'default_search': 'ytsearch5'
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch5:{search_query}", download=False)
                if 'entries' in info:
                    st.session_state["social_results"] = info['entries']
        except Exception as e:
            st.error(f"Error fetching content: {e}")

if "social_results" in st.session_state:
    st.success("Found matching social content!")
    for item in st.session_state["social_results"]:
        vid_title = item.get('title', 'Untitled')
        vid_id = item.get('id', '')
        vid_url = f"https://www.youtube.com/watch?v={vid_id}"
        
        st.write(f"**{vid_title}**")
        st.video(vid_url)
        
        if st.button(f"Select This Video #{vid_id}", key=vid_id):
            st.session_state["selected_video_url"] = vid_url
            st.success("Selected! Proceed to Step 2 to edit.")
