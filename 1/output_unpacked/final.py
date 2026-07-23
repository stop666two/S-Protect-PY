import hashlib
from pathlib import Path


def sha256_file(file_path):
    digest = hashlib.sha256()
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    for file_path in Path(".").iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".md":
            print(f"{file_path.name}\t{file_path.stat().st_size}\t{sha256_file(file_path)}")


if __name__ == "__main__":
    main()