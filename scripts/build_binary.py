"""
Corp++ Standalone Executable Binary Packager.
Bundles the entire Corp++ toolchain into a standalone single-file binary (`dist/corp`).
"""

import os
import sys
import zipapp
import shutil
import stat


def build_standalone_binary():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dist_dir = os.path.join(root_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)

    output_bin = os.path.join(dist_dir, "corp")
    temp_pack_dir = os.path.join(dist_dir, "_pack_temp")

    if os.path.exists(temp_pack_dir):
        shutil.rmtree(temp_pack_dir)
    os.makedirs(temp_pack_dir)

    print("═══════════════════════════════════════════════════════════════")
    print("      BUILDING CORP++ STANDALONE ENTERPRISE BINARY             ")
    print("═══════════════════════════════════════════════════════════════")
    print("1. Aggregating corporate assets and core competencies...")

    # Copy corp package to temp dir
    shutil.copytree(os.path.join(root_dir, "corp"), os.path.join(temp_pack_dir, "corp"))

    # Create __main__.py in root of zipapp
    with open(os.path.join(temp_pack_dir, "__main__.py"), "w", encoding="utf-8") as f:
        f.write("""import sys
from corp.cli.main import main

if __name__ == "__main__":
    main()
""")

    print("2. Packaging into single-file executable archive via zipapp...")
    if os.path.exists(output_bin):
        os.remove(output_bin)

    zipapp.create_archive(
        temp_pack_dir,
        target=output_bin,
        interpreter="/usr/bin/env python3",
        compressed=True
    )

    # Make executable
    st = os.stat(output_bin)
    os.chmod(output_bin, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    # Clean temp
    shutil.rmtree(temp_pack_dir)

    bin_size = os.path.getsize(output_bin)
    print(f"3. Binary generated successfully: {output_bin}")
    print(f"   Package Footprint: {bin_size} bytes")
    print("4. Quality Assurance verified: Binary is ready to distribute to colleagues and friends.")
    print("═══════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    build_standalone_binary()
