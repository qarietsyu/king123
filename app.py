import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="YouTube Video Summarizer", page_icon="🎬")
st.title("🎬 YouTube Video Summarizer")
st.write("Paste a public YouTube link and get an instant AI summary.")

url = st.text_input("Paste a YouTube link")
style = st.selectbox(
    "Summary style",
    ["Short (3 bullets)", "Detailed", "Explain like I'm 12"],
)
minutes = st.slider("Only summarize the first X minutes (faster)", 1, 20, 5)


def clean_url(link):
    link = link.strip()
    if "youtu.be/" in link:
        video_id = link.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return link.split("&")[0]


if st.button("Summarize") and url:
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
                        types.Part(
                            text=f"Summarize this video. Style: {style}. "
                            "Include a one-line title and 3 key takeaways."
                        ),
                    ]
                ),
                config=types.GenerateContentConfig(
                    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW
                ),
            )
            st.success(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
