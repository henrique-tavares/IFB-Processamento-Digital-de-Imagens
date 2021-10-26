from typing import Tuple, Optional
from itertools import product, islice
from PIL import Image
import sys
from os import path


def validate_args() -> Optional[Tuple[str, str, int, str]]:
    try:
        image_in = sys.argv[1]
        text = sys.argv[2]
        bits_level = int(sys.argv[3])
        image_out = sys.argv[4]

        if not path.exists(path.join(path.curdir, image_in)):
            raise FileNotFoundError("First argument (image_in) invalid")

        if not path.exists(path.join(path.curdir, text)):
            raise FileNotFoundError("Second argument (text_in) invalid")

        if bits_level < 0 or bits_level > 3:
            raise ValueError("Third argument (bits_level) must be between 0 and 3")

    except IndexError:
        print(f"Expected 4 arguments, but got {len(sys.argv) - 1}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except ValueError as e:
        print(e)

    else:
        if image_in == image_out:
            print("Warning: image_in and image_out are the same. image_in will be overwritten.", end="\n\n")

        return image_in, text, bits_level, image_out


def transform_pixel(image: Image, coordinate: Tuple[int, int], bit_plane: int, bit: str) -> Tuple[int, int, int]:
    pixel = image.getpixel(coordinate)
    pixel_binary = f"{pixel[bit_plane]:08b}"
    pixel_binary_transformed = pixel_binary[:-1] + bit
    pixel_transformed = pixel[:bit_plane] + tuple([int(pixel_binary_transformed, base=2)]) + pixel[(bit_plane + 1) :]

    return pixel_transformed


if __name__ == "__main__":

    args = validate_args()
    if args is None:
        exit(0)

    image_in_arg, text_arg, bits_level, image_out = args

    with Image.open(image_in_arg) as image_in, open(text_arg) as text_file:
        image_pixels = image_in.height * image_in.width

        text = text_file.read()
        text_filled = text.ljust(image_pixels)
        text_bytearray = bytearray(text, "utf-8")

        text_binary = "".join(f"{byte:08b}" for byte in text_bytearray)

        if (bits_level > 3 and len(text_binary) > (image_pixels * 3)) or len(text_binary) > (image_pixels):
            print("Error: The text does not fit into the image")
            exit(0)

        if bits_level != 3:
            for (x, y), bit in zip(product(range(image_in.height), range(image_in.width)), text_binary):
                pixel_transformed = transform_pixel(image_in, (x, y), bits_level, bit)

                image_in.putpixel((x, y), pixel_transformed)

        else:
            for (x, y), bit_index in zip(
                product(range(image_in.height), range(image_in.width)), islice(range(len(text_binary)), 0, None, 3)
            ):
                try:
                    for i in range(3):
                        pixel_transformed = transform_pixel(image_in, (x, y), i, text_binary[bit_index + i])

                        image_in.putpixel((x, y), pixel_transformed)

                except IndexError:
                    pass

        if not image_out.endswith(".png"):
            image_out += ".png"

        image_in.save(path.join(path.curdir, image_out))
