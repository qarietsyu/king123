# 🎬 YouTube Video Summarizer

A simple AI app that summarizes public YouTube videos using Google Gemini Flash. Built with Streamlit and deployed on Streamlit Community Cloud.

## Features
- Paste any public YouTube link
- Choose a summary style: Short, Detailed, or Explain like I'm 12
- Get a title and key takeaways in seconds

## Files
- `app.py` – the Streamlit app
- `requirements.txt` – Python dependencies
- `README.md` – this file

## Run locally
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a file at `.streamlit/secrets.toml` and add:
   ```
   GEMINI_API_KEY = "your-key-here"
   ```
3. Start the app:
   ```
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud
1. Push these three files to a GitHub repository.
2. Go to https://share.streamlit.io and click **New app**.
3. Select your repository, branch, and `app.py`.
4. Open **Advanced settings → Secrets** and add:
   ```
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy**.

## Get a Gemini API key
Create a free key at https://aistudio.google.com/apikey

## Notes
- The video must be public or unlisted.
- Very long videos may be slow. Try videos of 3 to 10 minutes.
- Never commit your API key to GitHub. Always use Streamlit Secrets.
