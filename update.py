import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw

API_KEY = os.environ["TMDB_API_KEY"]

# Create canvas
WIDTH = 1920
HEIGHT = 1080

canvas = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 10))

# Get trending content
url = f"https://api.themoviedb.org/3/trending/all/week?api_key={API_KEY}"

data = requests.get(url).json()

results = data["results"][:30]

x = 0
y = 0

CARD_W = 320
CARD_H = 180

for item in results:

    backdrop = item.get("backdrop_path")

    if not backdrop:
        continue

    img_url = f"https://image.tmdb.org/t/p/w780{backdrop}"

    try:
        response = requests.get(img_url)

        img = Image.open(BytesIO(response.content)).convert("RGB")

        img = img.resize((CARD_W, CARD_H))

        # Slight random rotation
        angle = random.randint(-8, 8)

        rotated = img.rotate(angle, expand=True)

        canvas.paste(rotated, (x, y))

        x += 280

        if x > WIDTH - CARD_W:
            x = 0
            y += 200

        if y > HEIGHT:
            break

    except:
        pass

# Dark overlay
overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 90))
canvas = canvas.convert("RGBA")
canvas.alpha_composite(overlay)

# Save image
os.makedirs("posters", exist_ok=True)

canvas.convert("RGB").save("posters/latest.jpg", quality=95)

print("Banner created.")
