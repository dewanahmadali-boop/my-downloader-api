from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/get-link")
def get_link(url: str):
    if not url:
        return JSONResponse(status_code=400, content={"status": "error", "message": "URL missing"})

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
            download_url = info.get('url')

            if not download_url:
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('url') and f.get('vcodec') != 'none':
                        download_url = f.get('url')
                        break

            if download_url:
                return {
                    "status": "success",
                    "title": title,
                    "url": download_url
                }
            else:
                return JSONResponse(status_code=404, content={"status": "error", "message": "Link not found"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
