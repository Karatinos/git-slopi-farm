#!/usr/bin/env python3
"""
Расшифровка перехваченного письма ВОССТАНОВЛЕННЫМ ключом d.

Игрок сначала запускает attack_client.py и восстанавливает d (строка "hex : 0x.."),
затем этим d и файлом-конвертом расшифровывает письмо:

    python3 solve_flag.py <d_hex> <intercepted.txt>

Схема (та же, что в encrypt.py / make_challenge.py):
    KEK = VKO_GOSTR3410_2012_512(d, E, ukm)      # RFC 7836, Streebog-512 от d*E
    plaintext = Kuznyechik-CTR(key=KEK, iv=iv, ct)
"""
import sys

import gost
from gostcrypto import gostcipher, gosthash


def streebog512(b):
    h = gosthash.new("streebog512")
    h.update(bytearray(b))
    return bytes(h.digest())


def vko512(scalar, Q, ukm, a, p, q):
    fb = (p.bit_length() + 7) // 8
    K = gost.multiply_point((ukm * scalar) % q, Q, a, p)
    return streebog512(K[0].to_bytes(fb, "little") + K[1].to_bytes(fb, "little"))


def kuznechik_ctr(key, iv, data):
    c = gostcipher.new("kuznechik", bytearray(key[:32]),
                       gostcipher.MODE_CTR, init_vect=bytearray(iv))
    return bytes(c.encrypt(bytearray(data)))


def parse(path):
    d = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        d[k.strip()] = v.strip()
    return d


def main():
    if len(sys.argv) < 3:
        print("usage: python3 solve_flag.py <d_hex> <intercepted.txt>")
        sys.exit(1)
    d = int(sys.argv[1], 16)                            # принимает 0x... и голый hex
    env = parse(sys.argv[2])
    E = (int(env["Ex"], 16), int(env["Ey"], 16))
    ukm = int(env["ukm"], 16)
    iv = bytes.fromhex(env["iv"])
    ct = bytes.fromhex(env["ct"])

    p, a, b, m, q, G = gost.id_tc26_gost_3410_12_512_paramSetA()
    KEK = vko512(d, E, ukm, a, p, q)                    # общий ключ = VKO(d, E)
    pt = kuznechik_ctr(KEK, iv, ct)

    print("=" * 60)
    print("РАСШИФРОВАННОЕ ПИСЬМО:")
    print("=" * 60)
    try:
        sys.stdout.write(pt.decode("utf-8"))
    except UnicodeDecodeError:
        sys.stdout.buffer.write(pt)
    print()


if __name__ == "__main__":
    main()
