# Download series opening and endings

import requests
import os
from pathlib import Path
from pydub import AudioSegment

def get_themes(mal_id):
	response = requests.post("https://themes.moe/api/themes/search", json=[mal_id])
	
	if len(response.json()) == 0:
		return False
	
	themes = response.json()[0]["themes"]

	for theme in themes:
		theme_type = theme["themeType"]
		theme_url = theme["mirror"]["mirrorURL"]
		file_name = theme_url.rsplit('/', 1)[1]

		mp3_file_name = f"{Path(file_name).stem}.mp3"
		
		theme_folder = None

		if "OP" in theme_type:
			theme_folder = "./openings"
		elif "ED" in theme_type:
			theme_folder = "./endings"
	
		mp3_path = f"{theme_folder}/{mp3_file_name}"
		video_path = f"{theme_folder}/{file_name}"

		headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4521.0 Safari/537.36 Edg/93.0.910.5"}
		response = requests.get(theme_url, allow_redirects=True, headers=headers, stream=True)

		video_file = open(video_path, "wb")
		for chunk in response.iter_content(chunk_size=1024*1024): 
			video_file.write(chunk)

		AudioSegment.from_file(video_path).export(mp3_path, format="mp3")
		os.remove(video_path)
	
	return True