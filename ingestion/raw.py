import os
import gzip

def to_rows(path: str):
    try:
        files = os.listdir(path)
        rows = []

        for file in files:
            file_path = os.path.join(path, file)

            if file.endswith(".gz"):
                opener = gzip.open
            else:
                opener = open

            with opener(file_path, mode="rt", encoding="utf-8") as f:
                rows.extend(f.readlines())

        return rows

    except OSError as e:
        print("Erreur lors de la lecture des fichiers :", e)
        return []

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "..", "data")
  
    print(to_rows(DATA_DIR)[:10])

    print(to_rows(DATA_DIR)[:10])