import os
import random
class init_spam:
    def __init__(self):
        pass
    def create_folders(self, amount, debug=False):
        if debug==True:
            print(f"Creating {amount} folders...")
            exit()
        else:
            for i in range(amount):
                try:
                    os.makedirs(random.randint(196, 9138476519387465), exist_ok=True)
                except PermissionError:
                    pass
