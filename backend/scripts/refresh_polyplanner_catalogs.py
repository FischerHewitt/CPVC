from pathlib import Path
from urllib.request import urlopen


SOURCE_URL = "https://api.polyplanner.pro/catalogs"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "polyplanner" / "catalogs.json"


def main() -> None:
    with urlopen(SOURCE_URL, timeout=60) as response:
        payload = response.read()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(payload)
    print(f"Wrote {len(payload):,} bytes to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
