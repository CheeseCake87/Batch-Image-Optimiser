from pathlib import Path

import click
from PIL import Image

CWD = Path.cwd()
IMAGES_DIR = CWD / "images"
OPTIMISED_DIR = CWD / "optimised"

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

if not IMAGES_DIR.exists():
    IMAGES_DIR.mkdir()

if not OPTIMISED_DIR.exists():
    OPTIMISED_DIR.mkdir()


def _process_images(images_dir: Path, optimised_dir: Path, dpi: int = 72, max_vector: int = None,
                    extension: str = ".jpg"):
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension not allowed {extension}")

    ext = extension.replace(".", "")

    for image in images_dir.iterdir():
        if image.suffix.lower() in ALLOWED_EXTENSIONS:
            img = Image.open(image)

            width, height = img.size

            # get dpi of image
            image_dpi = img.info.get("dpi", (72, 72))[0]

            print(f"OG | {image.name} | {image.stat().st_size / 1000} kb | {image_dpi} dpi")

            if dpi and dpi < image_dpi:
                img = img.resize((dpi, dpi))

            if max_vector:
                if width > height:
                    if width > max_vector:
                        img = img.resize((max_vector, int(max_vector * img.height / img.width)))
                else:
                    if height > max_vector:
                        img = img.resize((int(max_vector * img.width / img.height), max_vector))

            img.save(optimised_dir / f"{image.stem}_optimised.{ext}", ext)

            img.close()

            new_image = optimised_dir / f"{image.stem}_optimised.{ext}"
            new_img = Image.open(new_image).info.get("dpi", (72, 72))[0]

            print(f"IO | {new_image.name} | {new_image.stat().st_size / 1000} kb | {new_img} dpi")


@click.group("cli")
def cli():
    pass


@cli.command("to-webp", short_help="Convert images to webp")
@click.option("--dpi", default=72, type=int)
@click.option("--max-vector", "-mv", default=None, type=int)
def to_webp(dpi: int = 72, max_vector: int = None):
    _process_images(IMAGES_DIR, OPTIMISED_DIR, dpi, max_vector, ".webp")


@cli.command("to-jpg", short_help="Convert images to jpg")
@click.option("--dpi", default=72, type=int)
@click.option("--max-vector", "-mv", default=None, type=int)
def to_jpg(dpi: int = 72, max_vector: int = None):
    _process_images(IMAGES_DIR, OPTIMISED_DIR, dpi, max_vector, ".jpg")


@cli.command("to-png", short_help="Convert images to png")
@click.option("--dpi", default=72, type=int)
@click.option("--max-vector", "-mv", default=None, type=int)
def to_png(dpi: int = 72, max_vector: int = None):
    _process_images(IMAGES_DIR, OPTIMISED_DIR, dpi, max_vector, ".png")


if __name__ == "__main__":
    cli()
