import yt_dlp

class Mix:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url
        self.items = []

    def load(self):
        extract_opts = {
            'extract_flat': 'in_playlist',
        }
        with yt_dlp.YoutubeDL(extract_opts) as ydl:
            response = ydl.extract_info(
                        self.url, download = False)
            self.items = response['entries']
