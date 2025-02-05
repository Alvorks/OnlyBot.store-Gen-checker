import requests
import urllib3
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration de base
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generer_code():
    caracteres = string.ascii_letters + string.digits  # Generation du code
    return ''.join(random.choices(caracteres, k=25))


def check_key(code):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        url = f"https://onlybot.store/api/login_updater.php?key={code}&hwid="
        resp = requests.get(url, verify=False, timeout=10)
        if "ok connection" in resp.text:
            print(f"Nouveau hit : {code}")
            with open("valide.txt", "a") as fichier_valide:
                fichier_valide.write(code + "\n")
            return True
        else:
            print(f"Fail : {code}")
            return False
    except Exception as e:
        print(f"Erreur avec le code {code} : {str(e)}")
        return False


def main():
    while True:
        # Génération des codes
        nombre = int(input("Combien de codes voulez-vous générer ? "))
        codes = [generer_code() for _ in range(nombre)]

        # On sauvegarde dans le fichier
        with open("onlyauth.txt", "w") as fichier:
            for code in codes:
                fichier.write(code + "\n")

        print(f"{nombre} codes ont été générés et sauvegardés dans onlyauth.txt")

        # On choisit le nombre de threads
        nombre_threads = int(input("Combien de threads voulez-vous utiliser ? "))

        # Lecture des codes et vérification multithread
        print("Démarrage du checker...")
        with open("onlyauth.txt", "r") as fichier:
            codes_a_verifier = [ligne.strip() for ligne in fichier]

        with ThreadPoolExecutor(max_workers=nombre_threads) as executor:
            futures = [executor.submit(check_key, code) for code in codes_a_verifier]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Erreur lors de l'exécution d'un thread : {str(e)}")

        print("Toutes les clés ont été vérifiées. Les clés valides sont enregistrées dans valide.txt.")

        # On recommence
        restart = input("Voulez-vous générer et vérifier de nouveaux codes ? (oui/non) ").strip().lower()
        if restart != "oui":
            break


if __name__ == "__main__":
    main()
