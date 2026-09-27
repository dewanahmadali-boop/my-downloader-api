from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Video')
            formats_list = []

            for f in info.get('formats', []):
                # Filter useful video and audio streams
                ext = f.get('ext')
                vcodec = f.get('vcodec')
                acodec = f.get('acodec')
                
                if ext == 'mp4' or (vcodec != 'none' and acodec != 'none'):
                    resolution = f.get('format_note') or f.get('resolution') or 'Unknown'
                    filesize = f.get('filesize') or f.get('filesize_approx') or 0
                    
                    # Convert bytes to MB
                    size_mb = round(filesize / (1024 * 1024), 1) if filesize else 0.0
                    size_str = f"~{size_mb} MB" if size_mb > 0 else "Size Unknown"
                    
                    download_url = f.get('url')
                    if download_url and ('1080p' in str(resolution) or '720p' in str(resolution) or '480p' in str(resolution) or '360p' in str(resolution)):
                        formats_list.append({
                            "quality": f"{resolution} ({ext.upper()}) - {size_str}",
                            "url": download_url
                        })

            # Fallback if specific formats aren't neatly tagged
            if not formats_list and 'url' in info:
                formats_list.append({
                    "quality": "Default Quality",
                    "url": info['url']
                })

            return jsonify({
                "status": "success",
                "title": title,
                "formats": formats_list
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
