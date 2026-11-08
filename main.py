from ingestion import raw
from processing import extract_transform
from processing import geo_location
import os
from serving import dashboard


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    rows = raw.to_rows(DATA_DIR)

    echecs = extract_transform.extract_from_rows(rows)

    tentatives = extract_transform.extract_attempts(rows)
    #Graphe 1
    ip_counts = extract_transform.count_by_ip(echecs)
    country_counts = geo_location.count_by_country(ip_counts)
    first_six_countries = dict(list(country_counts.items())[:6])
    dashboard.plot_failed_by_country(first_six_countries)

    # Graphe 2
    success_counts = extract_transform.count_success_by_user(tentatives)
    first_six_success = dict(list(success_counts.items())[:6])
    dashboard.plot_success_by_user(first_six_success)

    #Graphe 3 
    invalid_counts = extract_transform.count_failed_invalid_user(tentatives)
    first_six = dict(list(invalid_counts.items())[:6])

    dashboard.plot_invalid_user(first_six)

    print(invalid_counts)

    print(tentatives)