from urllib import request
from bs4 import BeautifulSoup
import lxml
from PIL import Image
import os

import time


def count_words(url):
    print(f"Counting words at {url}")

    start = time.time()

    r = request.urlopen(url)

    soup = BeautifulSoup(r.read().decode(), "lxml")

    paragraphs = " ".join([p.text for p in soup.find_all("p")])

    word_count = {}

    for i in paragraphs.split():
        if i not in word_count:
            word_count[i] = 1
        else:
            word_count[i] += 1

    end = time.time()

    time_elapsed = end - start

    print(word_count)
    print(f"Total words: {len(word_count)}")
    print(f"Time elapsed: {time_elapsed}")

    return len(word_count)


def create_image_set(image_dir, image_name):
    start = time.time()

    thumb = 30, 30
    small = 540, 540
    medium = 768, 786
    large = 1080, 1080
    xl = 1200, 1200

    image = Image.open(os.path.join(image_dir, image_name))

    image_ext = image_name.split(".")[-1]
    image_name = image_name.split(".")[0]

    ### THUMBNAIL ###
    thumbnail_image = image.copy()
    thumbnail_image.thumbnail(thumb, Image.LANCZOS)
    thumbnail_image.save(
        f"{os.path.join(image_dir, image_name)}-thumbnail.{image_ext}",
        optimize=True,
        quality=95,
    )

    ### SMALL ###
    small_image = image.copy()
    small_image.thumbnail(small, Image.LANCZOS)
    small_image.save(
        f"{os.path.join(image_dir, image_name)}-540.{image_ext}",
        optimize=True,
        quality=95,
    )

    ### MEDIUM ###
    medium_image = image.copy()
    medium_image.thumbnail(medium, Image.LANCZOS)
    medium_image.save(
        f"{os.path.join(image_dir, image_name)}-768.{image_ext}",
        optimize=True,
        quality=95,
    )

    ### LARGE ###
    large_image = image.copy()
    large_image.thumbnail(large, Image.LANCZOS)
    large_image.save(
        f"{os.path.join(image_dir, image_name)}-1080.{image_ext}",
        optimize=True,
        quality=95,
    )

    ### XL ###
    xl_image = image.copy()
    xl_image.thumbnail(xl, Image.LANCZOS)
    xl_image.save(
        f"{os.path.join(image_dir, image_name)}-1200.{image_ext}",
        optimize=True,
        quality=95,
    )

    end = time.time()

    time_elapsed = end - start

    print(f"Task complete in: {time_elapsed}")

    return True
