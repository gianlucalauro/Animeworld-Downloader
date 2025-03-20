import os
import re
from datetime import datetime
from flask import Blueprint, jsonify, request
import animeworld as aw

api_bp = Blueprint('api', __name__)

@api_bp.route("/api/search", methods=["GET"])
def search_api():
    query = request.args.get("q", "")
    results = aw.find(query)
    return jsonify(results)

@api_bp.route("/api/download", methods=["POST"])
def anime_api():
    data = request.get_json()
    anime_link = data.get("link")
    selected_episodes = data.get("episodes")

    strm = request.args.get("strm", "false")

    if not anime_link:
        return jsonify({"error": "Nessun link fornito"}), 400

    result = aw.Anime(anime_link)

    if selected_episodes:
        episodes = result.getEpisodes(selected_episodes)
    else:
        episodes = result.getEpisodes()

    anime_name = sanitize_filename(result.getName())

    download_path = os.path.join("download", anime_name)
    os.makedirs(download_path, exist_ok=True)

    for ep in episodes:
        print(f"Downloading episode {ep.number}.")

        if strm == "true":
            download_strm(ep, download_path, f"{anime_name} - EP{ep.number}")
        else:
            ep.download(folder=download_path, hook=my_hook)

        print(f"Download completed for episode {ep.number}.")

    return jsonify({"result": "downloads completed successfully"})


def download_strm(episode, download_path, name):
    file_link = episode.links[0].fileLink()
    file_path = f"{download_path}/{name}.strm"
    with open(file_path, 'w') as file:
        file.write(file_link)
    print(f"File .strm salvato in: {file_path}")

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def my_hook(d):
    if d['status'] == 'downloading':
        out = "{filename}:\n[{bar}][{percentage:^6.1%}]\n{downloaded_bytes}/{total_bytes} in {elapsed:%H:%M:%S} (ETA: {eta:%H:%M:%S})\x1B[3A"

        width = 70

        d['elapsed'] = datetime.utcfromtimestamp(d['elapsed'])
        d['eta'] = datetime.utcfromtimestamp(d['eta'])
        d['bar'] = '#'*int(width*d['percentage']) + ' '*(width-int(width*d['percentage']))

        print(out.format(**d))

    elif d['status'] == 'finished':
        print('\n\n\n')
