from itertools import product
from pathlib import Path


from PIL import Image, ImageChops


def summarise(img: Image.Image) -> Image.Image:
    """Summarise an image into a 16 x 16 image."""
    resized = img.resize((16, 16))
    return resized


def difference(img1: Image.Image, img2: Image.Image) -> float:
    """Find the difference between two images."""

    diff = ImageChops.difference(img1, img2)

    acc = 0
    width, height = diff.size
    for w, h in product(range(width), range(height)):
        r, g, b = diff.getpixel((w, h))
        acc += (r + g + b) / 3 / 255

    diff = acc / (width * height)
    return diff


def explore_directory(path: Path) -> None:
    """Find images in a directory and compare them all."""

    files = list(path.glob("*.jpg")) + list(path.glob("*.jpeg")) + list(path.glob("*.png"))
    diffs = {}

    for file1, file2 in product(files, repeat=2):
        key = tuple(sorted([str(file1), str(file2)]))
        if key in diffs or key[0] == key[1]:
            continue

        small1 = summarise(Image.open(file1))
        small2 = summarise(Image.open(file2))
        diff = difference(small1, small2)
        print(key, diff)
        diffs[key] = diff

    print()
    print("Near-duplicates found:")
    print("======================")
    for key, diff in diffs.items():
        if diff < 0.07:
            print(key)


if __name__ == "__main__":
    explore_directory(Path("dublin"))
