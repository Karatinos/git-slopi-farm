# Ephemeral sandbox image for the execution plane.
# Build:  docker build -t slopi-farm-sandbox:latest farm/sandbox
# The container is run per attempt with --network none, cap-drop ALL,
# read-only rootfs and a tmpfs /work (see farm/sandbox/docker.py).
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        binutils file xxd unzip binwalk foremost exiftool \
        curl grep ripgrep coreutils \
    && rm -rf /var/lib/apt/lists/*

# Common CTF python tooling (crypto/reverse helpers). Kept light on purpose;
# heavy tools (ghidra/angr) are added per-category when the swarm needs them.
RUN pip install --no-cache-dir pycryptodome sympy pwntools requests

WORKDIR /work
CMD ["sleep", "3600"]
