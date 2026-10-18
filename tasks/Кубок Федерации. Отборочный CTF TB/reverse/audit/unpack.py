#!/usr/bin/env python3

from pathlib import Path
import struct


INPUT = Path("files/WorkstationAudit.exe")
OUTPUT = Path("files/WorkstationAudit.mem")


def u16(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def u64(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<Q", data, offset)[0]


def decrypt_lcg(source: bytes, seed: int) -> bytes:
    output = bytearray(len(source))
    state = seed & 0xFFFFFFFF
    for index, value in enumerate(source):
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        output[index] = value ^ (state >> 24)
    return bytes(output)


def map_pe(data: bytes) -> tuple[bytearray, int]:
    pe_offset = u32(data, 0x3C)
    section_count = u16(data, pe_offset + 6)
    optional_size = u16(data, pe_offset + 20)
    optional = pe_offset + 24
    image_base = u64(data, optional + 24)
    image_size = u32(data, optional + 56)
    headers_size = u32(data, optional + 60)
    image = bytearray(image_size)
    image[:headers_size] = data[:headers_size]

    section_table = optional + optional_size
    for index in range(section_count):
        header = section_table + 40 * index
        virtual_size = u32(data, header + 8)
        virtual_address = u32(data, header + 12)
        raw_size = u32(data, header + 16)
        raw_offset = u32(data, header + 20)
        copy_size = min(raw_size, virtual_size or raw_size)
        if copy_size:
            image[virtual_address : virtual_address + copy_size] = data[
                raw_offset : raw_offset + copy_size
            ]
    return image, image_base


def decrypt_metadata(image: bytearray, meta_rva: int = 0x110000) -> bytearray:
    metadata = bytearray(image[meta_rva : meta_rva + 336])
    state = 2050694495
    offset = 0
    while offset != len(metadata):
        while True:
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            if not 64 <= offset <= 67:
                break
            offset += 1
        metadata[offset] ^= state >> 24
        offset += 1
    image[meta_rva : meta_rva + len(metadata)] = metadata
    return metadata


def main() -> None:
    packed = INPUT.read_bytes()
    image, image_base = map_pe(packed)
    metadata = decrypt_metadata(image)

    stored_base = u64(metadata, 0x00)
    source_va = u64(metadata, 0x18)
    original_entry = u32(metadata, 0x30)
    seed = u32(metadata, 0x44)
    chunk_count = u32(metadata, 0x48)
    if stored_base != image_base:
        raise ValueError("unexpected image base")

    source_rva = source_va - image_base
    chunks = []
    for index in range(chunk_count):
        descriptor = 0x50 + 16 * index
        target_rva, size, source_offset, protection = struct.unpack_from(
            "<IIII", metadata, descriptor
        )
        source = bytes(image[source_rva + source_offset : source_rva + source_offset + size])
        plaintext = decrypt_lcg(source, seed + target_rva)
        image[target_rva : target_rva + size] = plaintext
        chunks.append((target_rva, size, source_offset, protection))

    OUTPUT.write_bytes(image)
    print(f"image_base=0x{image_base:x}")
    print(f"entry=0x{image_base + original_entry:x}")
    for target_rva, size, source_offset, protection in chunks:
        print(
            f"chunk rva=0x{target_rva:x} size=0x{size:x} "
            f"source=0x{source_offset:x} protection=0x{protection:x}"
        )
    print(f"wrote {OUTPUT} ({len(image)} bytes)")


if __name__ == "__main__":
    main()
