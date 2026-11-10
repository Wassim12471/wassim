import os
import csv
import pymysql

# Configuration MariaDB / MySQL
MARIADB_HOST = os.getenv("MARIADB_HOST", "localhost")
MARIADB_PORT = int(os.getenv("MARIADB_PORT", "3306"))
MARIADB_DB = os.getenv("MARIADB_DB", "log_security")
MARIADB_USER = os.getenv("MARIADB_USER", "root")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "")

CSV_PATH = os.path.join(os.path.dirname(__file__), "security_logs.csv")


def get_connection():
    """
    Retourne une connexion active vers la base MariaDB.
    """
    return pymysql.connect(
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
        database=MARIADB_DB,
        cursorclass=pymysql.cursors.DictCursor
    )


def init_db():
    """
    Crée la base de données et la table security_logs dans MariaDB.
    """
    # Connexion sans spécifier la base pour pouvoir la créer si inexistante
    root_conn = pymysql.connect(
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD
    )
    with root_conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MARIADB_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    root_conn.commit()
    root_conn.close()

    # Création de la table
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS security_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                month VARCHAR(10),
                day VARCHAR(10),
                time VARCHAR(20),
                event VARCHAR(50),
                user VARCHAR(100),
                ip VARCHAR(45),
                country VARCHAR(10),
                city VARCHAR(100),
                raw TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
    conn.commit()
    conn.close()


def save_logs(logs_list):
    """
    Insère une liste de dictionnaires de logs dans MariaDB.
    """
    if not logs_list:
        return 0

    init_db()
    conn = get_connection()
    inserted = 0

    query = """
        INSERT INTO security_logs (month, day, time, event, user, ip, country, city, raw)
        VALUES (%(month)s, %(day)s, %(time)s, %(event)s, %(user)s, %(ip)s, %(country)s, %(city)s, %(raw)s)
    """

    with conn.cursor() as cur:
        cur.executemany(query, logs_list)
        inserted = cur.rowcount

    conn.commit()
    conn.close()
    return inserted


def export_to_csv(logs_list, csv_path=CSV_PATH):
    """
    Exporte les logs nettoyés en fichier CSV.
    """
    if not logs_list:
        return

    keys = ["month", "day", "time", "event", "user", "ip", "country", "city"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(logs_list)


def get_top_attackers(limit=5):
    """
    Requête analytique : Récupère les IPs avec le plus de tentatives d'intrusion.
    """
    conn = get_connection()
    results = []
    with conn.cursor() as cur:
        query = """
            SELECT ip, country, city, COUNT(*) as attempts
            FROM security_logs
            WHERE event IN ('FAILED_PASSWORD', 'INVALID_USER') AND ip IS NOT NULL
            GROUP BY ip, country, city
            ORDER BY attempts DESC
            LIMIT %s
        """
        cur.execute(query, (limit,))
        rows = cur.fetchall()
        # Convertir en liste de tuples (ip, country, city, attempts)
        results = [(r["ip"], r["country"], r["city"], r["attempts"]) for r in rows]
    conn.close()
    return results


if __name__ == "__main__":
    init_db()
    print("Connexion et table MariaDB 'security_logs' vérifiées avec succès !")
