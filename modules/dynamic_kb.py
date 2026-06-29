import os
import hashlib

HASH_FILE = "vector_store/file_hashes.txt"
DOCS_FOLDER = "datasets/custom_docs"


def calculate_folder_hash():
    hash_obj = hashlib.md5()

    for root, _, files in os.walk(DOCS_FOLDER):
        for file in sorted(files):
            path = os.path.join(root, file)

            with open(path, "rb") as f:
                while chunk := f.read(4096):
                    hash_obj.update(chunk)

    return hash_obj.hexdigest()


def has_knowledge_base_changed():
    current_hash = calculate_folder_hash()

    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
        return True

    with open(HASH_FILE, "r") as f:
        old_hash = f.read().strip()

    if current_hash != old_hash:
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
        return True

    return False