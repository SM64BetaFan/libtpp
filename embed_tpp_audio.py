#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
SOUND_DIR = ROOT / "tpp" / "build" / "us" / "sound"
ASSETS = {
    "ctl": "sound_data.ctl",
    "tbl": "sound_data.tbl",
    "sequences": "sequences.bin",
    "bank_sets": "bank_sets",
}


def write_c_array(output, symbol, data):
    output.write(f"const uint8_t g_tpp_audio_{symbol}[] =\n")
    if not data:
        output.write('    "";\n')
    else:
        for offset in range(0, len(data), 32):
            chunk = data[offset : offset + 32]
            escaped = "".join(f"\\x{byte:02x}" for byte in chunk)
            output.write(f'    "{escaped}"\n')
        output.write("    ;\n")
    output.write(
        f"const size_t g_tpp_audio_{symbol}_size = "
        f"sizeof(g_tpp_audio_{symbol}) - 1;\n\n"
    )


def main():
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} OUTPUT.c")

    output_path = Path(sys.argv[1])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    asset_paths = {name: SOUND_DIR / filename for name, filename in ASSETS.items()}
    if not all(path.is_file() for path in asset_paths.values()):
        asset_data = {name: b"" for name in ASSETS}
    else:
        asset_data = {name: path.read_bytes() for name, path in asset_paths.items()}

    with output_path.open("w", newline="\n") as output:
        output.write('#include "tpp_audio_assets.h"\n\n')
        for name, data in asset_data.items():
            write_c_array(output, name, data)


if __name__ == "__main__":
    main()
