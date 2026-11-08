import gzip
import os
"""
read data logs from data directory as rows "lgnes"
"""

def toRows(path):
    files = os.listdir(path)
    
    for file in files:
        file_path=path+'/'+file
        openner = gzip.open(filename=file_path,mode='rt',encoding='utf-8') if file.endswith(".gz") else open(file_path) 
        with openner as f:

            rows=f.readlines()


    return rows
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR , "..","data")
    print(toRows("DATA_DIR") [:10])