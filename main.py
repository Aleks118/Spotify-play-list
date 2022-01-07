import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "input_your client id"
CLIENT_SECRET = "input your secret"
URL_REDIRECT = "http://example.com"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
year = date.split("-")[0]

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)

Billboard_webpage = response.text

songs = BeautifulSoup(Billboard_webpage, "html.parser")

song_titles = songs.find_all(name="h3",id="title-of-a-story", class_= "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
top100 = []

for names in song_titles:
    song = names.get_text().strip("\n")
    top100.append(song)

# print (top100)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)


song_uris = []

for song in top100:
    result = sp.search(q=f"track:{song}, year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(song_uris)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped")

new_playlist = sp.user_playlist_create(user=user_id, name=f"Billboard {date}", public=False, collaborative=False)
new_id = new_playlist["id"]
sp.playlist_add_items(playlist_id=new_id, items=song_uris, position=None)
