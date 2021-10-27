from typing import Any, Callable, Generator, Iterable, Tuple, Optional
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
            print(
                "Warning: image_in and image_out are the same. image_in will be overwritten.",
                end="\n\n",
            )

        return image_in, text, bits_level, image_out


def transform_pixel(image: Image, coordinate: Tuple[int, int], bit_plane: int, bit: str) -> Tuple[int, int, int]:
    pixel = image.getpixel(coordinate)
    pixel_binary = f"{pixel[bit_plane]:08b}"
    pixel_binary_transformed = pixel_binary[:-1] + bit
    pixel_transformed = pixel[:bit_plane] + tuple([int(pixel_binary_transformed, base=2)]) + pixel[(bit_plane + 1) :]

    # print(
    #     pixel,
    #     pixel[bit_plane],
    #     pixel_binary,
    #     "+",
    #     bit,
    #     "->",
    #     pixel_binary_transformed,
    #     int(pixel_binary_transformed, base=2),
    #     pixel_transformed,
    # )

    return pixel_transformed


def pop_with_generator(
    iterable: Iterable,
    generator: Generator,
    default: Any,
    handle_fallback: Callable[[Iterable, Any], None],
) -> Any:
    if len(iterable) == 0:
        value = next(generator, default)
        handle_fallback(iterable, value)

    return iterable.pop(0)


if __name__ == "__main__":

    args = validate_args()
    if args is None:
        exit(0)

    image_in_arg, text_arg, bits_level, image_out = args

    with Image.open(image_in_arg) as image_in, open(text_arg) as text_file:
        image_pixels = image_in.height * image_in.width

        text = text_file.read()
        text_bytearray = bytearray(text, "utf-8")
        text_bytearray_generator = (byte for byte in text_bytearray)
        text_bits = len(text_bytearray) * 8

        if (bits_level > 3 and text_bits > (image_pixels * 3)) or text_bits > image_pixels:
            print("Error: The text does not fit into the image")
            exit(0)

        bit_buffer = []
        for (x, y) in product(range(image_in.height), range(image_in.width)):
            if bits_level == 3:
                for i in range(3):
                    bit = pop_with_generator(
                        bit_buffer,
                        text_bytearray_generator,
                        0,
                        lambda iterable, byte: iterable.extend(f"{byte:08b}"),
                    )
                    pixel_transformed = transform_pixel(image_in, (x, y), i, bit)
                    image_in.putpixel((x, y), pixel_transformed)
            else:
                bit = pop_with_generator(
                    bit_buffer,
                    text_bytearray_generator,
                    0,
                    lambda iterable, byte: iterable.extend(f"{byte:08b}"),
                )
                pixel_transformed = transform_pixel(image_in, (x, y), bits_level, bit)
                image_in.putpixel((x, y), pixel_transformed)

        if not image_out.endswith(".png"):
            image_out += ".png"

        image_in.save(path.join(path.curdir, image_out))
