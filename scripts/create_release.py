import os
import sys
import shutil
import zipfile
import tarfile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.build_binary import build_standalone_binary
from corp import __version__


def create_release_bundles():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dist_dir = os.path.join(root_dir, "dist")
    release_dir = os.path.join(dist_dir, "release")
    os.makedirs(release_dir, exist_ok=True)

    # 1. Build binary
    build_standalone_binary()

    bin_path = os.path.join(dist_dir, "corp")
    tar_path = os.path.join(release_dir, f"corp-v{__version__}-standalone.tar.gz")
    zip_path = os.path.join(release_dir, f"corp-v{__version__}-standalone.zip")

    # Create tar.gz
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(bin_path, arcname="corp")
        tar.add(os.path.join(root_dir, "README.md"), arcname="README.md")
        tar.add(os.path.join(root_dir, "LICENSE"), arcname="LICENSE")
        tar.add(os.path.join(root_dir, "examples"), arcname="examples")

    # Create zip
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(bin_path, arcname="corp")
        zipf.write(os.path.join(root_dir, "README.md"), arcname="README.md")
        zipf.write(os.path.join(root_dir, "LICENSE"), arcname="LICENSE")
        for root, _, files in os.walk(os.path.join(root_dir, "examples")):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                zipf.write(full_path, arcname=rel_path)

    print("═══════════════════════════════════════════════════════════════")
    print(f"       CORP++ RELEASE v{__version__} BUNDLES CREATED          ")
    print("═══════════════════════════════════════════════════════════════")
    print(f"Tarball: {tar_path} ({os.path.getsize(tar_path)} bytes)")
    print(f"Zip:     {zip_path} ({os.path.getsize(zip_path)} bytes)")
    print("═══════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    create_release_bundles()
