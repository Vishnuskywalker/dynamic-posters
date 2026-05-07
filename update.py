import requests
import random
import os

API_KEY = os.environ["TMDB_API_KEY"]

url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={API_KEY}"

data = requests.get(url).json()

results = data["results"]

show = random.choice(results)

backdrop = show.get("backdrop_path")

if backdrop:
    img_url = f"https://image.tmdb.org/t/p/original{backdrop}"

    img = requests.get(img_url).content

    with open("posters/anime.jpg", "wb") as f:
        f.write(img)

    print("Poster updated.")
else:
    print("No backdrop found.")
