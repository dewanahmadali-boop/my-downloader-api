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
            download_url = info.get('url') # Direct stream url

            if not download_url:
                # Fallback to formats if direct url is missing
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('url') and f.get('vcodec') != 'none':
                        download_url = f.get('url')
                        break

            if download_url:
                return jsonify({
                    "status": "success",
                    "title": title,
                    "url": download_url
                })
            else:
                return jsonify({"status": "error", "message": "Link not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
