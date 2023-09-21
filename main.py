import os
import json

if os.path.exists("secret.py"):
    from secret import (
        nb_user_id,
        nb_password,
        nlic_user_id,
        nlic_password,
        nlic_user_token,
    )
else:
    nb_user_id = json.loads(os.environ.get("nb_user_id"))
    nb_password = os.environ.get("nb_password")
    nlic_user_id = json.loads(os.environ.get("nlic_user_id"))
    nlic_password = os.environ.get("nlic_password")
    nlic_user_token = json.loads(os.environ.get("nlic_user_token"))
from nblib import get_nblib_loan
from nlic import get_nlic_loan


def main():
    nblib_loan_dict = get_nblib_loan(nb_user_id, nb_password)
    nlic_loan_dict = get_nlic_loan(nlic_user_id, nlic_password, nlic_user_token)

    print(nblib_loan_dict, nlic_loan_dict)

    users = []
    for user_dict in nblib_loan_dict["users"]:
        for num, count in user_dict.items():
            users.append(f"{num}(甬):{count}本")
    for user_dict in nlic_loan_dict["users"]:
        for num, count in user_dict.items():
            users.append(f"{num}(鄞):{count}本")

    books = []
    for book_dict in nblib_loan_dict["books"]:
        book_title = book_dict["title"]
        return_date = book_dict["returndate"][:10]
        if len(book_title) > 7:
            book_title = book_title[:3] + "…" + book_title[-3:]
        user_name_last_char = book_dict["user_name"][-1]
        if book_dict["renewable"]:
            books.append(f"{return_date} {book_title} (甬-{user_name_last_char}-可续借)")
        else:
            books.append(f"{return_date} {book_title} (甬-{user_name_last_char})")
    for book_dict in nlic_loan_dict["books"]:
        book_title = book_dict["title"]
        return_date = book_dict["returndate"][:10]
        if len(book_title) > 7:
            book_title = book_title[:3] + "…" + book_title[-3:]
        user_name_last_char = book_dict["user_name"][-1]
        if book_dict["renewable"]:
            books.append(f"{return_date} {book_title} (鄞-{user_name_last_char}-可续借)")
        else:
            books.append(f"{return_date} {book_title} (鄞-{user_name_last_char})")

    from collections import Counter

    dates = []
    for book_dict in nblib_loan_dict["books"]:
        return_date = book_dict["returndate"][:10]
        dates.append(return_date)
    for book_dict in nlic_loan_dict["books"]:
        return_date = book_dict["returndate"][:10]
        dates.append(return_date)
    dates = Counter(dates)

    return_string = ""
    for user in sorted(users, reverse=True):
        return_string += f"\n{user}"
    for book in sorted(books, reverse=True):
        return_string += f"\n{book}"
    for date in sorted(dates, reverse=True):
        return_string += f"\n{date}:{dates[date]}本"

    print(return_string)
    return return_string
