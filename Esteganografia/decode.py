from typing import Tuple, Optional
from itertools import product
from PIL import Image
import sys
from os import path


def validate_args() -> Optional[Tuple[str, int, str]]:
    try:
        image_out = sys.argv[1]
        bits_level = int(sys.argv[2])
        text_out = sys.argv[3]

        if not path.exists(path.join(path.curdir, image_out)):
            raise FileNotFoundError("First argument (image_out) invalid")

        if bits_level < 0 or bits_level > 3:
            raise ValueError("Third argument (bits_level) must be between 0 and 3")

    except IndexError:
        print(f"Expected 3 arguments, but got {len(sys.argv) - 1}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except ValueError as e:
        print(e)

    else:
        return image_out, bits_level, text_out


if __name__ == "__main__":

    args = validate_args()
    if args is None:
        exit(0)

    image_out_arg, bits_level, text_out_arg = args

    with Image.open(path.join(path.curdir, image_out_arg)) as image_out, open(text_out_arg, "wb") as text:
        text_bytearray = bytearray()

        bit_buffer = []
        for (x, y) in product(range(image_out.height), range(image_out.width)):
            pixel = image_out.getpixel((x, y))

            if bits_level == 3:
                for i in range(3):
                    byte = pixel[i]
                    byte_str = f"{byte:08b}"
                    bit = byte_str[-1]
                    bit_buffer.append(bit)
            else:
                byte = pixel[bits_level]
                byte_str = f"{byte:08b}"
                bit = byte_str[-1]
                bit_buffer.append(bit)

            if len(bit_buffer) >= 8:
                byte_str = "".join(bit_buffer[:8])
                byte = int(byte_str or "0", base=2)
                text_bytearray.append(byte)

                bit_buffer = bit_buffer[8:]

        stripped_text_bytearray = text_bytearray.strip(b"\x00")
        text_bytes = bytes(stripped_text_bytearray)
        text.write(text_bytes)
