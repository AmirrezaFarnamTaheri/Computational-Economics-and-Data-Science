#!/usr/bin/env python3
"""
Download Script for Open-Source Educational Images
Downloads CC-licensed and open-source images from web sources
"""

import requests
from pathlib import Path
import time

IMAGE_BASE = Path(__file__).parent.parent / "images"

# ============================================================================
# IMAGE SOURCES (All CC-Licensed or Open Source)
# ============================================================================

DOWNLOAD_MANIFEST = {
    # Sutton & Barto RL Figures (Educational Use)
    "machine_learning/rl/agent_environment_loop.png": {
        "url": "http://incompleteideas.net/book/first/ebook/figtmp1.png",
        "license": "Educational Use",
        "source": "Sutton & Barto RL Book"
    },

    # Economic Diagrams from EconGraphs (Open Source)
    "micro_macro/micro/supply_demand.png": {
        "url": "https://www.econgraphs.org/graphs/v1/micro/supply_and_demand/supply_and_demand?textbook=varian",
        "license": "Open Source",
        "source": "EconGraphs.org"
    }

    # Add more images as needed...
}

def download_image(filename, info):
    """Download a single image with proper attribution"""
    filepath = IMAGE_BASE / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Downloading {filename}...")
        response = requests.get(info['url'], timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        # Create attribution file
        attribution_file = filepath.parent / f"{filepath.stem}_LICENSE.txt"
        with open(attribution_file, 'w') as f:
            f.write(f"Source: {info['source']}\\n")
            f.write(f"License: {info['license']}\\n")
            f.write(f"URL: {info['url']}\\n")

        print(f"  ✓ Downloaded: {filename}")
        return True

    except Exception as e:
        print(f"  ✗ Failed: {filename} - {e}")
        return False

def main():
    print("\\n" + "="*70)
    print("DOWNLOADING OPEN-SOURCE EDUCATIONAL IMAGES")
    print("="*70 + "\\n")

    successful = 0
    failed = 0

    for filename, info in DOWNLOAD_MANIFEST.items():
        if download_image(filename, info):
            successful += 1
        else:
            failed += 1
        time.sleep(1)  # Be respectful to servers

    print("\\n" + "="*70)
    print(f"✓ Successfully downloaded: {successful}")
    print(f"✗ Failed: {failed}")
    print("="*70 + "\\n")

if __name__ == "__main__":
    main()