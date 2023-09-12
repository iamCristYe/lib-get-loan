from secret import nb_user_id, nb_password, nlic_user_id, nlic_password, nlic_user_token
from nblib import get_nb_lib_loan
from nlic import get_nlic_loan

get_nb_lib_loan(nb_user_id, nb_password)
get_nlic_loan(nlic_user_id, nlic_password, nlic_user_token)
