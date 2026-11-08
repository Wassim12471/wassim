import requests
from requests import reponse
def get_location(ip):
    reponse=requests.get("https://ipinfo.io/"+ip+"/json")
    if reponse.status_code == 200:
        return reponse.json()
    else:
        return None


if __name__ == "__main__" :
    print(get_location('109.199.110.135'))