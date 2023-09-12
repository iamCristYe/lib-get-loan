from secret import nb_user_id, nb_password, nlic_user_id, nlic_password, nlic_user_token
from nblib import get_nblib_loan
from nlic import get_nlic_loan

nblib_loan = get_nblib_loan(nb_user_id, nb_password)
nlic_loan = get_nlic_loan(nlic_user_id, nlic_password, nlic_user_token)

for book in sorted(nblib_loan + nlic_loan):
    print(book)
