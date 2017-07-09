import pafy
import os

songs = """
www.youtube.com/watch?v=PT2_F-1esPk
https://www.youtube.com/watch?v=ek7cafqgYB4
https://www.youtube.com/watch?v=HQnC1UHBvWA
https://www.youtube.com/watch?v=s8XIgR5OGJc
https://www.youtube.com/watch?v=lEi_XBg2Fpk
https://www.youtube.com/watch?v=a52Ul2AM92c
https://www.youtube.com/watch?v=ULHeRdgeT54
https://www.youtube.com/watch?v=5JxgDJvqGmM
https://www.youtube.com/watch?v=2pY_WobtVuQ
https://www.youtube.com/watch?v=ALZHF5UqnU4
https://www.youtube.com/watch?v=tD4HCZe-tew
https://www.youtube.com/watch?v=qDRORgoZxZU
https://www.youtube.com/watch?v=si81bIoZRJQ
https://www.youtube.com/watch?v=AeGfss2vsZg
https://www.youtube.com/watch?v=wvzfOyW0ZMo
https://www.youtube.com/watch?v=SMs0GnYze34
https://www.youtube.com/watch?v=BPzG12uXSwQ
https://www.youtube.com/watch?v=85ftfVUTzM4
https://www.youtube.com/watch?v=Trzzg6qL7Ic
https://www.youtube.com/watch?v=BC_Ya4cY8RQ
https://www.youtube.com/watch?v=PZvFFezMTOU
https://www.youtube.com/watch?v=uW__O0QruV4
https://www.youtube.com/watch?v=mOKqNxN4jWM
https://www.youtube.com/watch?v=-WlAJxk8OhU
https://www.youtube.com/watch?v=Po7e5jD18l0
https://www.youtube.com/watch?v=a59gmGkq_pw
https://www.youtube.com/watch?v=sO9cBXRcBvo
https://www.youtube.com/watch?v=K_yBUfMGvzc
https://www.youtube.com/watch?v=ANIkOH0Hb9Y
https://www.youtube.com/watch?v=xAIoh9rxRi8
https://www.youtube.com/watch?v=Nng_zGDhHgg
https://www.youtube.com/watch?v=Nng_zGDhHgg
https://www.youtube.com/watch?v=hgKDu5pp_fU
https://www.youtube.com/watch?v=iob9UYFwFwk
https://www.youtube.com/watch?v=Io0fBr1XBUA
https://www.youtube.com/watch?v=XPzCzaBhF7s
https://www.youtube.com/watch?v=u3VFzuUiTGw
https://www.youtube.com/watch?v=pnSZbl8fTHM
https://www.youtube.com/watch?v=AUU7xY7R5s0
https://www.youtube.com/watch?v=B2m_WnXjqnM
https://www.youtube.com/watch?v=rTlqY9i7Gn4
https://www.youtube.com/watch?v=dMMUH_ZpbB0
https://www.youtube.com/watch?v=Ly7uj0JwgKg
https://www.youtube.com/watch?v=SXiSVQZLje8
https://www.youtube.com/watch?v=MMaXUVyJBos
https://www.youtube.com/watch?v=SgO9yYlS9QY
https://www.youtube.com/watch?v=aH9eOTGE-Es
https://www.youtube.com/watch?v=mgEixhE3Oms
https://www.youtube.com/watch?v=PyfYvLeG0tc
https://www.youtube.com/watch?v=P3CxhBIrBho
https://www.youtube.com/watch?v=eC-F_VZ2T1c
https://www.youtube.com/watch?v=juiq5YZlw0U
https://www.youtube.com/watch?v=lY2yjAdbvdQ
https://www.youtube.com/watch?v=jsbeemdD2rQ
https://www.youtube.com/watch?v=jGflUbPQfW8&list=RDjGflUbPQfW8#t=9
https://www.youtube.com/watch?v=YqeW9_5kURI&index=2&list=RDjGflUbPQfW8
https://www.youtube.com/watch?v=fRh_vgS2dFE&index=5&list=RDjGflUbPQfW8
https://www.youtube.com/watch?v=7PCkvCPvDXk&list=RDjGflUbPQfW8&index=16
https://www.youtube.com/watch?v=euCqAq6BRa4&index=20&list=RDjGflUbPQfW8
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
def get(songurl):

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
        return

    path = root + artist
    if not os.path.exists(path):
        print_v("making dir for <" + artist + ">")
        os.makedirs(path, exist_ok=True)
    try:
        bestaudio = yt.getbestaudio(preftype="m4a")
        bestaudio.download(filepath=path+ "/" + title + "." + bestaudio.extension, quiet=True)
    except FileExistsError:
        print_v("You already have <" + title + ">")
    except FileNotFoundError:
        print_v("error with <" + title + ">")
        unsure_songs.append(songurl)


for songurl in songs.split("\n"):
    get(songurl)
    
while True:
    try:
        get(input("Song URL: "))
    except:
        print_v("There was an error")