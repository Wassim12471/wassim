import requests
import os
import logging

# --- AJOUT : logging dyal had module (fichier mستقل) ---
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("geo_location")
logger.setLevel(logging.INFO)
_handler = logging.FileHandler("logs/geo_location.log", encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(_handler)

URL_IPINFO = 'http://ipinfo.io'
def get_location(ip):
    # --- AJOUT : timeout=5 ---
    response= requests.get(URL_IPINFO + "/" + ip+'/json', timeout=5)
    if response.status_code == 200:
        return response.json()
    # --- AJOUT : on log les réponses non 200 (ex: 429 = limite atteinte) ---
    logger.warning("%s : status %s", ip, response.status_code)


def get_country(ip):
    """
    in: une adresse ip
    out: code pays (ex: 'FR') ou 'Inconnu' si ipinfo ne répond pas
    """
    try:
        location = get_location(ip)
    except requests.RequestException as e:
        # --- AJOUT : logging au lieu de print ---
        logger.error("%s error : %s", ip, e)
        return 'Inconnu'
    if location and 'country' in location:
        return location['country']
    return 'Inconnu'


def count_by_country(ip_counts):
    """
    in: dictionnaire {ip: nombre d'échecs}
    out: dictionnaire {pays: nombre d'échecs}
    """
    pays_des_ip = {}   # mémoire : chaque ip n'est demandée qu'une seule fois à ipinfo
    resultat = {}
    total = len(ip_counts)
    for i, ip in enumerate(ip_counts, start=1):
        if ip not in pays_des_ip:
            pays_des_ip[ip] = get_country(ip)
        pays = pays_des_ip[ip]
        resultat[pays] = resultat.get(pays, 0) + ip_counts[ip]
        if i % 100 == 0:
            print(f'  {i}/{total} adresses ip traitées...')
    logger.info("%d ip traitées", total)
    return resultat

if __name__ == "__main__":
    print(get_location('176.32.193.16'))
    print(get_country('176.32.193.16'))