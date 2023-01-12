import re

import lyricsgenius
import pandas as pd

client_access_token = 'wmX3PDrznbEoOk_ls7E9eTB5MqWup05Ny7ggt8LimQgQqK-UlzHst6otZOGRex0Q'
artist_name = 'Eminem'
csv = f'../lyrics/{artist_name}_lyrics.csv'
max_song_count = 100

LyricsGenius = lyricsgenius.Genius(client_access_token)

retry = 0

while retry < 5:
    try:
        artist = LyricsGenius.search_artist(artist_name, max_songs=max_song_count)
        break
    except Exception as e:
        retry += 1
        print(e)


def extract_verses(raw_lyrics):
    l = re.split(r"(\[.+\])\n", raw_lyrics)
    s = '\n'.join(l)
    s = s.replace('[', '\n[')
    l = re.findall(r"(\[Verse.+\]\n)((.+\n)+)", s)
    o = ""
    for match in l:
        o += match[0] + match[1] + '\n'
    return o


def preprocess(lyrics):
    verses = extract_verses(lyrics)
    verses = "\n".join(verses.split("\n")[1:])
    verses = re.sub(r"(\(.+\))", "", verses)
    verses = re.sub(r"(\[.+\])", "", verses)
    verses = verses.replace("\n\n", "\n")
    return re.sub(r"\d+Embed", "", verses)


d = {
    "name": [artist.name for song in artist.songs],
    "title": [song.title for song in artist.songs],
    "lyrics": [preprocess(song.lyrics) for song in artist.songs]
}
df = pd.DataFrame(d)

try:
    external = pd.read_csv(csv, sep=';')
    df = pd.concat([df, external], ignore_index=True).drop_duplicates().reset_index(drop=True)
except Exception as e:
    print(e)
    print("*****CSV empty or corrupted!*****")
df.to_csv(csv, sep=';', encoding='utf-8')
