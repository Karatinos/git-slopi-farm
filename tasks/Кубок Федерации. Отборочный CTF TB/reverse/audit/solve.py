#!/usr/bin/env python3

from pathlib import Path
import struct

from unpack import OUTPUT as MEMORY_IMAGE
from unpack import main as unpack


IMAGE_BASE = 0x140000000
CHECK_TABLE_RVA = 0xDA060
CHECK_COUNT = 8
CHECK_SIZE = 32
COMMAND_POINTER_OFFSET = 16
TOKEN_RVA = 0xDA160
TOKEN_SIZE = 34


def read_c_string(image: bytes, rva: int) -> bytes:
    end = image.index(0, rva)
    return image[rva:end]


def derive_seed(image: bytes) -> int:
    state = 0xCBF29CE484222325
    prime = 0x100000001B3
    for index in range(CHECK_COUNT):
        entry = CHECK_TABLE_RVA + index * CHECK_SIZE
        command_va = struct.unpack_from(
            "<Q", image, entry + COMMAND_POINTER_OFFSET
        )[0]
        command = read_c_string(image, command_va - IMAGE_BASE)
        for value in command + b"\0":
            state = ((state ^ value) * prime) & 0xFFFFFFFFFFFFFFFF
    return state


def decrypt_token(image: bytes, state: int) -> str:
    multiplier = 0x5851F42D4C957F2D
    increment = 0x14057B7EF767814F
    plaintext = bytearray()
    for value in image[TOKEN_RVA : TOKEN_RVA + TOKEN_SIZE]:
        state = (multiplier * state + increment) & 0xFFFFFFFFFFFFFFFF
        plaintext.append(value ^ (state >> 56))
    return plaintext.decode("ascii")


def main() -> None:
    if not MEMORY_IMAGE.exists():
        unpack()
    image = MEMORY_IMAGE.read_bytes()
    seed = derive_seed(image)
    token = decrypt_token(image, seed)
    if not token.startswith("flag{") or not token.endswith("}"):
        raise ValueError("decoded token has an unexpected format")
    print(token)


if __name__ == "__main__":
    main()
