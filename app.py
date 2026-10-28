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

if st.button("Summarize") and url:
    with st.spinner("Watching the video..."):
        try:
            response = client.models.generate_content(
                model="model="gemini-3.8-flash",",
                contents=types.Content(
                    parts=[
                        types.Part(file_data=types.FileData(file_uri=url)),
                        types.Part(
                            text=f"Summarize this video. Style: {style}. "
                            "Include a one-line title and 3 key takeaways."
                        ),
                    ]
                ),
            )
            st.success(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
