import hashlib

def calculate_md5(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

if __name__ == "__main__":
    file_path = "main.py"

    md5_result = calculate_md5(file_path)
    print(f"MD5 hash [{file_path}]: {md5_result}")
