import os
import json

# from secret import nb_user_id, nb_password, nlic_user_id, nlic_password, nlic_user_token
from nblib import get_nblib_loan
from nlic import get_nlic_loan

nb_user_id = json.loads(os.environ.get("nb_user_id"))
nb_password = os.environ.get("nb_password")
nlic_user_id = json.loads(os.environ.get("nlic_user_id"))
nlic_password = os.environ.get("nlic_password")
nlic_user_token = json.loads(os.environ.get("nlic_user_token"))


def main():
    nblib_loan = get_nblib_loan(nb_user_id, nb_password)
    nlic_loan = get_nlic_loan(nlic_user_id, nlic_password, nlic_user_token)
    return_string = ""
    for book in sorted(nblib_loan + nlic_loan, reverse=True):
        return_string += f"\n{book}"

    print(return_string)
    return return_string
