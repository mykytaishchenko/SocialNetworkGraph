from social_network_graph.data_loader import Loader
from social_network_graph.soc_graph import SocialGraph

if __name__ == "__main__":
    Loader.path = "../data"

    cont = True

    while cont:
        accounts = input("Enter accounts you want to download: ").split()
        for account in accounts:
            if Loader.get(account) is not None:
                print(f"{account} account downloaded.")
        print("All accounts downloaded!")

        answer = input("Continue? ")
        if answer == "n" or answer.lower() == "no":
            cont = False
