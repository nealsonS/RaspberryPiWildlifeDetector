#!/usr/bin/env bash
set -e

sudo apt-get update
sudo apt-get install -y libcap-dev
sudo apt-get install ffmpeg

# Install picamera2 from apt on Raspberry Pi OS; skip silently on other systems
if sudo apt-get install -y python3-picamera2 --no-install-recommends 2>/dev/null; then
    echo "picamera2 installed via apt"
else
    echo "python3-picamera2 not available via apt (non-Pi system); will install via pip"
fi

curl -LsSf https://astral.sh/uv/install.sh | sh

# Source uv into PATH — location varies by install method
if [ -f "$HOME/.local/bin/env" ]; then
    source "$HOME/.local/bin/env"
else
    export PATH="$HOME/.local/bin:$PATH"
fi

uv venv --python 3.11
source .venv/bin/activate

uv pip install .