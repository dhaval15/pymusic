from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import json
import yt_dlp
import os
import subprocess

def extract_info(id):
    extract_opts = {
    }
    with yt_dlp.YoutubeDL(extract_opts) as ydl:
        try: 
            response = ydl.extract_info(id, download = False)
            return response
        except:
            print(f'Unable to fetch data for {id}')

def infuse_info(file, info):
    mp3file = MP3(file, ID3=EasyID3)
    mp3file['ALBUM'] = info.get('album', '')
    mp3file['TITLE'] = info.get('title')
    artists = info.get('artist', '').split(',')
    mp3file['ARTIST'] = list(map(lambda x: x.strip(), artists))
    mp3file.save()

class YTInfo:
    def __init__(self, info_file: str, file_builder, outtmpl) -> None:
        self.info_file = info_file 
        self.file_builder = file_builder
        self.data = None
        self.outtmpl = outtmpl
    
    def load(self) -> None:
        if os.path.isfile(self.info_file):
            with open(self.info_file, 'r') as openfile:
                self.data = json.load(openfile)
        else:
            self.data = {}

    def get(self, id: str) -> dict:
        value = self.data.get(id) or extract_info(id)
        return value

    def save(self):
        if self.data is None:
            pass
        json_object = json.dumps(self.data, indent=4)
        with open(self.info_file, 'w+') as outfile:
            outfile.write(json_object)

    def infuse(self, id: str):
        info = self.get(id)
        if info is None:
            return False
        file = self.file_builder(id)
        if not os.path.isfile(file):
            return False
        infuse_info(file, info)
        return True

    def read(self, id: str):
        file = self.file_builder(id)
        mp3file = MP3(file, ID3=EasyID3)
        return mp3file

    def legacy(self, url: str):
        try:
            subprocess.call(['yt-dlp', '-r', '5M', '--embed-metadata', '--embed-thumbnail', '-x', '--audio-format', 'mp3', url, '-o', self.outtmpl])
            return True
        except:
            return False

    def exists(self, id):
        file = self.file_builder(id)
        return os.path.isfile(file)

    def download(self, url: str):
        download_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.outtmpl,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'FFmpegMetadata', 
                    'add_metadata': True,
                },
                {
                    'key': 'EmbedThumbnail', 
                    #'already_have_thumbnail': False,
                },
            ],
        }
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            try:
                ydl.download([url])
                return True
            except:
                return False

