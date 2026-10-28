import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=90000),
)

st.set_page_config(page_title="YouTube Video Summarizer", page_icon="🎬")
st.title("🎬 YouTube Video Summarizer")

style = st.selectbox(
    "Summary style",
    ["Short (3 bullets)", "Detailed", "Explain like I'm 12"],
)
prompt = (
    f"Summarize this. Style: {style}. "
    "Include a one-line title and 3 key takeaways."
)


def clean_url(link):
    link = link.strip()
    if "youtu.be/" in link:
        video_id = link.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return link.split("&")[0]


tab1, tab2 = st.tabs(["🔗 From YouTube link", "📝 From transcript (fast)"])

with tab1:
    url = st.text_input("Paste a YouTube link")
    minutes = st.slider("Only summarize the first X minutes", 1, 10, 2)
    if st.button("Summarize video") and url:
        with st.spinner("Watching the video..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=types.Content(
                        parts=[
                            types.Part(
                                file_data=types.FileData(file_uri=clean_url(url)),
                                video_metadata=types.VideoMetadata(
                                    start_offset="0s",
                                    end_offset=f"{minutes * 60}s",
                                ),
                            ),
                            types.Part(text=prompt),
                        ]
                    ),
                    config=types.GenerateContentConfig(
                        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW
                    ),
                )
                st.success(response.text)
            except Exception as e:
                st.error(f"Video method failed: {e}")
                st.info("Try a shorter video, or use the transcript tab instead.")

with tab2:
    transcript = st.text_area("Paste the video transcript or any text", height=250)
    if st.button("Summarize text") and transcript:
        with st.spinner("Summarizing..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"{prompt}\n\nText:\n{transcript}",
                )
                st.success(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
