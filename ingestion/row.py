
import gzip
import os

def toRows(path):
    rows = []

    files = os.listdir(path)

    for file in files:
        file_path = os.path.join(path, file)

        if file.endswith(".gz"):
            openner = gzip.open(
                file_path, mode="rt", encoding="utf-8"
            )
        else:
            openner = open(
                file_path, mode="r", encoding="utf-8"
            )

        with openner as f:
            rows.extend(f.readlines())

    return rows


if __name__ == '__main__':
    print("Current directory:", os.getcwd())
    print("Data exists:", os.path.exists("./data"))

    print(toRows("./data")[:10])
