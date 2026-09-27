from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server is running!"}

@app.get("/get-link")
def get_video_link(url: str):
    ydl_opts = {'skip_download': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            # Shobcheye bhalo mp4 ba stream link-ta khuje ber kora
            direct_url = ""
            for f in formats:
                if f.get('ext') == 'mp4' and f.get('url'):
                    direct_url = f.get('url')
                    break
            if not direct_url and formats:
                direct_url = formats[-1].get('url', '')
                
            title = info.get('title', 'Video')
            return {"status": "success", "title": title, "download_url": direct_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}
