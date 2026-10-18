
#!/usr/bin/env python3
"""
Эталонный солвер «Всё по ГОСТу».

Автоматически восстанавливает закрытый ключ получателя d (тайминг-утечка нонса →
HNP → решётка) и расшифровывает перехваченное письмо, выводя флаг. Основан на
реальном решении, а не на «зашитом» ответе: связывает attack_client.py (добыча d)
и solve_flag.py (VKO_512 + Кузнечик).

    python3 solver.py [intercepted.txt] [L]

По умолчанию intercepted.txt берётся из ../files/, L = 8.
Env: ORACLE_HOST (127.0.0.1)  ORACLE_PORT (31337)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    intercepted = (sys.argv[1] if len(sys.argv) > 1
                   else os.path.join(HERE, "..", "files", "intercepted.txt"))
    L = sys.argv[2] if len(sys.argv) > 2 else "8"

    print("[*] Восстанавливаем закрытый ключ d (тайминг -> HNP -> решётка)...",
          flush=True)
    att = subprocess.run(
        [sys.executable, os.path.join(HERE, "attack_client.py"), L],
        capture_output=True, text=True)
    sys.stdout.write(att.stdout)
    m = re.search(r"hex\s*:\s*(0x[0-9a-fA-F]+)", att.stdout)
    if not m:
        print("[!] Ключ восстановить не удалось.", file=sys.stderr)
        sys.exit(1)
    d = m.group(1)
    print(f"[+] d = {d}", flush=True)

    print("[*] Расшифровываем перехваченное письмо...", flush=True)
    dec = subprocess.run(
        [sys.executable, os.path.join(HERE, "solve_flag.py"), d, intercepted],
        capture_output=True, text=True)
    sys.stdout.write(dec.stdout)

    fm = re.search(r"flag\{[^}]*\}", dec.stdout)
    if fm:
        print(f"\n[+] FLAG: {fm.group(0)}")


if __name__ == "__main__":
    main()
