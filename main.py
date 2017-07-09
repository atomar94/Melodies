import pafy
import os

songs = """
www.youtube.com/watch?v=PT2_F-1esPk
https://www.youtube.com/watch?v=ek7cafqgYB4
https://www.youtube.com/watch?v=HQnC1UHBvWA
https://www.youtube.com/watch?v=s8XIgR5OGJc
"""
#songs="https://www.youtube.com/watch?v=otv7lJmLJtQ"
#unsure of their artist/title
unsure_songs = []

#root = "C:/users/alex/Music/Melodies/"
root = "./"
_verbose = True
def print_v(s):
    if _verbose:
        print(s)

_debug = True
def print_d(s):
    if _debug:
        print(s)

#return a tuple/3 (yt object, artist, title)
def getter(songurl):

    # Sanitize
    if not songurl.strip():
        return
    if songurl[0:8] == "https://":
        songurl = songurl[8:]

    # Get metadata from youtube
    artist = ""
    title = ""
    yt = None
    try:
        yt = pafy.new(songurl)
    except ValueError:
        print_v("Pafy can't parse the url: " + songurl)
        return

    if len(yt.title.split('-')) == 2:
        artist = yt.title.split('-')[0].strip()
        title = yt.title.split('-')[1].strip()
    else:
        unsure_songs.append(songurl)
        print_v("Could not parse artist/title from " + yt.title)
        artist = "Could Not Parse"
        title = yt.title.strip()
    return {"yt": yt, 
            "artist": artist, 
            "title": title}

def directory_constructor(metadatas):
    paths = []
    for m in metadatas:
        print_d(type(m))
        m['path'] = root + m['artist']
        paths.append(m['path'])

    print("Do you want to create these directories?")
    for p in paths:
        print(p)

    if input("[Y/n]").lower().strip() == "y":
        for m in metadatas:
            if not os.path.exists(m['path']):
                print_v("making dir for <" + m['artist'] + ">")
                os.makedirs(m['path'], exist_ok=True)
            try:
                bestaudio = m['yt'].getbestaudio(preftype="m4a")
                bestaudio.download(filepath=m['path'] + "/" + m['title'] + "." + bestaudio.extension, quiet=True)
            except FileExistsError:
                print_v("You already have <" + m['title'] + ">")
            except FileNotFoundError:
                print_v("error with <" + m['title'] + ">")
                unsure_songs.append(m['yt'].url)


song_data = []

for i, songurl in enumerate(songs.split("\n")):
    print_v("Parsing " + str(i) + " of " + str(len(songs.split("\n"))))
    metadata = getter(songurl)
    if metadata:
        song_data.append(metadata)

directory_constructor(song_data)

    
while True:
    try:
        getter(input("Song URL: "))
    except:
        exit()