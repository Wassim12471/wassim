# Pipeline Log Analyser





### Objectives
-Read and collect log files(ingestion)
-Extract useful information from logs.(processing)
-Analyse successful and dailed login attempts.
-Identify suspicious login attempts.
-Display statistics using graphs.(servong)
-Save analysis results using graphs.
-Save analysis results in JSON and CSV files(Storage)

### Technologies Used

-Python
-Regular expression (re)
-Requests
Logging
-OS
-Gzip
-Matplotlib
-JSON
-CSV

log_analisis/
│
├── ingestion/
│   
│   └── raw.py
│
├── processing/
│   ├── 
│   ├── extract_transform.py
│   ├── geo_location.py
│   └── geo_cache.py
│
├── serving/
│   ├──
│   └── dashboard.py
│
├── storage/
│   ├── __init__.py
│   ├── save_json.py
│   └── save_csv.py
│
├── data/
├── logs/
├── results/
├── main.py
└── README.md



# Results 
-Failed attempts by country
-Successful attempts by user
-Failed attempts with invalid users
-Graphs generated using Matplotlib
-JSON and CSV result files
