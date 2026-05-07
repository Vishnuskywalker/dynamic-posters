import requests
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageEnhance
import math
import os

# =========================
# CONFIG
# =========================

API_KEY = os.environ["TMDB_API_KEY"]

WIDTH = 1920
HEIGHT = 1080

CARD_W = 320
CARD_H = 180

OUTPUT = "latest_releases.jpg"

# =========================
# GET TRENDING CONTENT
# =========================

url = f"https://api.themoviedb.org/3/trending/all/week?api_key={API_KEY}"

data = requests.get(url).json()

results = data["results"][:40]

# =========================
# CREATE BACKGROUND
# =========================

canvas = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 12))
draw = ImageDraw.Draw(canvas)

# =========================
# DOWNLOAD IMAGES
# =========================

posters = []

for item in results:

    backdrop = item.get("backdrop_path")

    if not backdrop:
        continue

    img_url = f"https://image.tmdb.org/t/p/w780{backdrop}"

    try:
        img_data = requests.get(img_url, timeout=10).content

        img = Image.open(BytesIO(img_data)).convert("RGB")

        posters.append(img)

    except:
        pass

# =========================
# PLACE TILTED CARDS
# =========================

x_positions = list(range(-100, WIDTH, 260))
y_positions = list(range(-50, HEIGHT, 170))

random.shuffle(posters)

index = 0

for row, y in enumerate(y_positions):

    offset = 120 if row % 2 else 0

    for x in x_positions:

        if index >= len(posters):
            break

        img = posters[index]
        index += 1

        # Resize
        img = img.resize((CARD_W, CARD_H))

        # Darken slightly
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.88)

        # Rounded corners
        mask = Image.new("L", (CARD_W, CARD_H), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (0, 0, CARD_W, CARD_H),
            radius=18,
            fill=255
        )

        rounded = Image.new("RGBA", (CARD_W, CARD_H))
        rounded.paste(img, (0, 0))
        rounded.putalpha(mask)

        # Random rotation
        angle = random.uniform(-8, 8)

        rotated = rounded.rotate(
            angle,
            expand=True,
            resample=Image.Resampling.BICUBIC
        )

        # Paste position
        px = x + offset
        py = y

        canvas.paste(rotated, (px, py), rotated)

# =========================
# DARK OVERLAY
# =========================

overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 80))

canvas = Image.alpha_composite(
    canvas.convert("RGBA"),
    overlay
)

# =========================
# SAVE
# =========================

canvas.convert("RGB").save(
    OUTPUT,
    quality=95
)

print("Generated:", OUTPUT)
