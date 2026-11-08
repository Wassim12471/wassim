import matplotlib.pyplot as plt
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename="logs/dashboard.log",level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")

def plot_failed_by_country(country_counts):
    try:
        countries = list(country_counts.keys())
        attempts = list(country_counts.values())

        plt.figure(figsize=(5,5))
        plt.bar(countries, attempts, color="Red")
        plt.grid(axis="y", alpha=0.3)

        plt.title("Failed Attempts by Country")
        plt.xlabel("Country")
        plt.ylabel("Number of Failed Attempts")

        plt.tight_layout()

        logging.info("Graph 1 created successfully")
        plt.show()

    except Exception as e:
        logging.exception("Error creating Graph 1: %s", e)



def plot_success_by_user(user_counts):
    try:
        users = list(user_counts.keys())
        counts = list(user_counts.values())

        plt.figure(figsize=(5,5))
        plt.bar(users, counts, color="green")
        
        plt.title("Successful Attempts by User")
        plt.xlabel("User")
        plt.ylabel("Number of Successful Attempts")

        plt.tight_layout()
        logging.info("Graph 2 created successfully")
        plt.show()
    except Exception as e:
        logging.exception("Error in Graphe 2: %s",e)

def plot_invalid_user(invalid_counts):
    try:
     users = list(invalid_counts.keys())
     counts = list(invalid_counts.values())

     plt.figure(figsize=(5,5))

     plt.bar(users , counts , color="orange")
     plt.title("Failed counts with Invalid User")
     plt.xlabel("Invalid User")
     plt.ylabel("Numbre of Failed counts")

     plt.tight_layout()
     logging.info("Graph 3 created successfully")
     plt.show()
    except Exception as e:
        logging.exception("Error in Graphe 3: %s",e)






if __name__ == "__main__":

    test_data = {
        "France" : 120,
        "USA" : 85,
        "CN" : 200,
        "Maroc" : 45
    }
    test_users = {
        "admin" : 50,
        "root" : 20,
        "ubuntu" : 35
    }
    test_Invalid_user = {
         "test" : 12,
         "elana" : 114,
         "admin" : 10
    }
    plot_failed_by_country(test_data)

    plot_success_by_user(test_users)

    plot_invalid_user(test_Invalid_user)

    
