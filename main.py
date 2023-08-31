from yt_info import YTInfo
from mix import Mix
file = 'test/.meta.json'
def file_builder(id: str):
    return f'/home/dhaval/Music/{id}.mp3'
outtmpl = '/home/dhaval/Music/%(id)s.%(ext)s'
yt_info = YTInfo(file, file_builder, outtmpl)
yt_info.load()
#mix = Mix('Music', 'PLUcoirQnrSt-3YesjMGUZEqfGgPFIxWvp')
mix = Mix('Music', 'PLUcoirQnrSt-3YesjMGUZEqfGgPFIxWvp')
mix.load()

def check():
    count = 0
    for item in mix.items:
        if not yt_info.exists(item['id']):
            yt_info.legacy(item['url'])
            yt_info.infuse(item['id'])
            print(item['title'])
            count = count + 1
    print(f'{count} tracks unpulled')


def download():
    for item in mix.items:
        if not yt_info.exists(item['id']):
            yt_info.legacy(item['url'])
        yt_info.infuse(item['id'])
    yt_info.save()

check()
