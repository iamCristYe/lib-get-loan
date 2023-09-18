import time
import requests


def get_nlic_loan(user_id_list, pwd, token_list):
    nlic_list = []

    for i in range(len(user_id_list)):
        nlic_list += get_nlic_loan_per_user(user_id_list[i], pwd, token_list[i])

    return nlic_list


def get_nlic_loan_per_user(user_id, pwd, token):
    current_user_id = user_id

    # curl 'https://bopac.nlic.cn/api/tcc-opac-park/system/reader/login' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6' \
    # -H 'Connection: keep-alive' \
    # -H 'Content-Type: application/json;charset=UTF-8' \
    # -H 'DNT: 1' \
    # -H 'Origin: https://bopac.nlic.cn' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' \
    # -H 'sec-ch-ua: "Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "Windows"' \
    # --data-raw '{"rdid":"12345678","rdpasswd":"12345678"}' \
    # --compressed

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "DNT": "1",
        "Origin": "https://bopac.nlic.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }

    json_data = {
        "rdid": f"{current_user_id}",
        "rdpasswd": f"{pwd}",
    }

    response = requests.post(
        "https://bopac.nlic.cn/api/tcc-opac-park/system/reader/login",
        headers=headers,
        json=json_data,
    )

    # print(response.content)
    # b'{"code":200,"data":{"..."}'

    response_dict = response.json()
    # print(response_dict["data"]["realName"], response_dict["data"]["opacToken"])
    current_user_name = response_dict["data"]["rdname"]
    with open("log.txt", "a") as log:
        log.write(str(response_dict) + "\n")

    # curl 'https://bopac.nlic.cn/api/tcc-opac-park/loanWork/getLoanList' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6' \
    # -H 'Connection: keep-alive' \
    # -H 'Content-Type: application/json;charset=UTF-8' \
    # -H 'DNT: 1' \
    # -H 'OPAC-TOKEN: 12345678' \
    # -H 'Origin: https://bopac.nlic.cn' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' \
    # -H 'rdid: 12345678' \
    # -H 'sec-ch-ua: "Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "Windows"' \
    # --data-raw '{"rdid":"12345678","current":1,"size":10}' \
    # --compressed

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "DNT": "1",
        "OPAC-TOKEN": f"{token}",
        "Origin": "https://bopac.nlic.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "rdid": f"{current_user_id}",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    json_data = {"rdid": f"{current_user_id}", "current": 1, "size": 100}

    response = requests.post(
        "https://bopac.nlic.cn/api/tcc-opac-park/loanWork/getLoanList",
        headers=headers,
        json=json_data,
    )

    response_dict = response.json()
    # print(response_dict["data"])
    with open("log.txt", "a") as log:
        log.write(str(response_dict) + "\n")

    nlic_user_list = []

    if "records" in response_dict["data"]:
        print(
            f"{current_user_id:010d}在鄞州图书馆当前借阅{len(response_dict['data']['records']):02d}本。"
        )
        for book in response_dict["data"]["records"]:
            nlic_user_list.append(
                f"{book['returndate'][:10]} {book['title'][:16]} (鄞州图书馆:{current_user_name})"
            )
        # {"code":200,"data":{"..."},"desc":"操作成功"}

    else:
        print(f"{current_user_id:010d}在鄞州图书馆当前借阅00本。")

    return nlic_user_list
