import re
import os
import logging
"""
in: list of rows (lignes des fichiers auth.log)
out: liste des tentatives de connexion échouées (mois, jour, ip, nombre)
     + comptage des échecs par jour
"""

# --- AJOUT : logging (un fichier log par module) ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/extract_transform.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Table pour transformer le mois du log (Jan, Feb, ...) en numéro : sert au tri chronologique
MOIS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

# Exemples de lignes recherchées :
#   May 24 00:02:47 ns sshd[1098645]: Failed password for root from 45.148.10.147 port 8868 ssh2
#   May 24 01:14:12 ns sshd[1351821]: message repeated 4 times: [ Failed password for root from 45.148.10.147 port 8868 ssh2]
# (?P<repeat>...) est optionnel : présent seulement pour les lignes "message repeated N times"
pattern = re.compile(
    r'(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+\d{2}:\d{2}:\d{2}\s+\w+\s+sshd\[\d+\]:\s+'
    r'(message repeated (?P<repeat>\d+) times: \[\s*)?'
    r'Failed password for (invalid user )?\S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
)

# --- AJOUT : même regex mais qui capture aussi le user et "invalid user" ---
pattern_failed_detail = re.compile(
    r'(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+\d{2}:\d{2}:\d{2}\s+\w+\s+sshd\[\d+\]:\s+'
    r'(message repeated (?P<repeat>\d+) times: \[\s*)?'
    r'Failed password for (?P<invalid>invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
)

# --- AJOUT : connexions réussies ---
#   May 24 02:10:01 ns sshd[1234]: Accepted password for admin from 10.0.0.5 port 5555 ssh2
#   May 24 02:10:01 ns sshd[1234]: Accepted publickey for admin from 10.0.0.5 port 5555 ssh2
pattern_success = re.compile(
    r'(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+\d{2}:\d{2}:\d{2}\s+\w+\s+sshd\[\d+\]:\s+'
    r'(message repeated (?P<repeat>\d+) times: \[\s*)?'
    r'Accepted (?:password|publickey) for (?P<user>\S+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
)


def extract_from_rows(rows):
    """
    in: list of rows
    out: list de dictionnaires {'mois': 5, 'jour': 24, 'ip': '1.2.3.4', 'nb': 1}
    """
    # On colle toutes les lignes en un seul texte : finditer est plus efficace que findall
    texte = ''.join(rows)
    echecs = []
    for match in re.finditer(pattern, texte):
        # Une ligne "message repeated N times" représente N échecs, sinon 1 seul
        nb = int(match.group('repeat')) if match.group('repeat') else 1
        echecs.append({
            'mois': MOIS[match.group('month')],
            'jour': int(match.group('day')),
            'ip': match.group('ip'),
            'nb': nb,
        })
    return echecs


# --- AJOUT : extraction complète (échecs + réussites), ligne par ligne ---
def extract_attempts(rows):
    """
    in: list of rows
    out: list de dictionnaires
         {'mois': 5, 'jour': 24, 'ip': '1.2.3.4', 'user': 'root',
          'invalid_user': False, 'status': 'failed' ou 'success', 'nb': 1}
    """
    tentatives = []
    for ligne in rows:
        try:
            m = pattern_failed_detail.search(ligne)
            if m:
                tentatives.append({
                    'mois': MOIS[m.group('month')],
                    'jour': int(m.group('day')),
                    'ip': m.group('ip'),
                    'user': m.group('user'),
                    'invalid_user': m.group('invalid') is not None,
                    'status': 'failed',
                    'nb': int(m.group('repeat')) if m.group('repeat') else 1,
                })
                continue

            m = pattern_success.search(ligne)
            if m:
                tentatives.append({
                    'mois': MOIS[m.group('month')],
                    'jour': int(m.group('day')),
                    'ip': m.group('ip'),
                    'user': m.group('user'),
                    'invalid_user': False,
                    'status': 'success',
                    'nb': int(m.group('repeat')) if m.group('repeat') else 1,
                })
                continue

            # Ligne sshd liée à une connexion mais format non reconnu : on la log
            if 'sshd' in ligne and ('Failed' in ligne or 'Accepted' in ligne):
                logging.warning("Ligne non reconnue : %s", ligne.strip())
        except (KeyError, ValueError) as e:
            logging.error("Erreur sur la ligne %r : %s", ligne.strip(), e)

    logging.info("%d tentatives extraites de %d lignes", len(tentatives), len(rows))
    return tentatives


def count_by_ip(echecs):
    """
    in: list d'échecs (voir extract_from_rows)
    out: dictionnaire {ip: nombre d'échecs}
    """
    resultat = {}
    for echec in echecs:
        resultat[echec['ip']] = resultat.get(echec['ip'], 0) + echec['nb']
    return resultat


def count_by_day(echecs):
    """
    in: list d'échecs (voir extract_from_rows)
    out: dictionnaire {(mois, jour): nombre d'échecs}
    """
    resultat = {}
    for echec in echecs:
        cle = (echec['mois'], echec['jour'])
        resultat[cle] = resultat.get(cle, 0) + echec['nb']
    return resultat


# --- AJOUT : comptages pour les dashboards ---
def count_success_by_user(tentatives):
    """
    in: list de tentatives (voir extract_attempts)
    out: dictionnaire {user: nombre de connexions réussies}
    """
    resultat = {}
    for t in tentatives:
        if t['status'] == 'success':
            resultat[t['user']] = resultat.get(t['user'], 0) + t['nb']
    return resultat


def count_failed_invalid_user(tentatives):
    """
    in: list de tentatives (voir extract_attempts)
    out: dictionnaire {user: nombre d'échecs avec invalid user}
    """
    resultat = {}
    for t in tentatives:
        if t['status'] == 'failed' and t['invalid_user']:
            resultat[t['user']] = resultat.get(t['user'], 0) + t['nb']
    return resultat


if __name__ == "__main__":
    ligne = ['May 24 01:14:12 ns sshd[1351821]: message repeated 4 times: [ Failed password for root from 45.148.10.147 port 8868 ssh2]\n',
             'May 10 00:02:47 ns sshd[1098645]: Failed password for invalid user admin from 203.171.18.62 port 22 ssh2\n',
             'May 24 02:10:01 ns sshd[1234]: Accepted password for ubuntu from 10.0.0.5 port 5555 ssh2\n']
    echecs = extract_from_rows(ligne)
    print(echecs)
    print(count_by_day(echecs))

    # AJOUT : test des nouvelles fonctions
    tentatives = extract_attempts(ligne)
    print(tentatives)
    print(count_success_by_user(tentatives))
    print(count_failed_invalid_user(tentatives))