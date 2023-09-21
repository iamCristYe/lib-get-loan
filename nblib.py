import time
import random
import requests


def get_nblib_loan(user_id_list, pwd):
    # curl 'https://opac.nblib.cn/api/tcc-opac/999/system/user/getOpenApiAccessToken' \
    # -X 'POST' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'Accept-Language: zh-CN,zh;q=0.9' \
    # -H 'Connection: keep-alive' \
    # -H 'Content-Length: 0' \
    # -H 'DNT: 1' \
    # -H 'Origin: https://opac.nblib.cn' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' \
    # -H 'sec-ch-ua: "Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "Windows"' \
    # --compressed

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Origin": "https://opac.nblib.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.post(
        "https://opac.nblib.cn/api/tcc-opac/999/system/user/getOpenApiAccessToken",
        headers=headers,
    )
    response_dict = response.json()
    with open("log.txt", "a") as log:
        log.write(str(response_dict) + "\n")
    current_access_token = response_dict["data"]["token"]

    nblib_list = []

    for user_id in user_id_list:
        time.sleep(random.randint(3, 10))
        nblib_list += get_nblib_loan_per_user(user_id, pwd, current_access_token)

    return nblib_list


def get_nblib_loan_per_user(user_id, pwd, current_access_token):
    current_user_id = user_id

    # curl 'https://opac.nblib.cn/api/tcc-opac/999/system/user/login' \
    # -H 'ACCESS-TOKEN: 12345678' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6' \
    # -H 'Connection: keep-alive' \
    # -H 'Content-Type: application/json;charset=UTF-8' \
    # -H 'DNT: 1' \
    # -H 'Origin: https://opac.nblib.cn' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1' \
    # --data-raw '{"mobilePhone":"","password":"==","orgId":"623217618121138176","captchaCode":null,"captchaKey":"1c38071c-fb61-4f84-8663-46648cd3c00a"}' \
    # --compressed

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "DNT": "1",
        "Origin": "https://opac.nblib.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }

    json_data = {
        "mobilePhone": f"{current_user_id}",
        "password": f"{pwd}",
        "orgId": "623217618121138176",
        "captchaCode": None,
        "captchaKey": "1c38071c-fb61-4f84-8663-46648cd3c00a",
    }

    response = requests.post(
        "https://opac.nblib.cn/api/tcc-opac/999/system/user/login",
        headers=headers,
        json=json_data,
    )

    # print(response.content)
    # b'{"code":200,"data":{"..."}'

    response_dict = response.json()
    # print(response_dict["data"]["realName"], response_dict["data"]["opacToken"])
    current_user_name = response_dict["data"]["realName"]
    current_opac_token = response_dict["data"]["opacToken"]
    with open("log.txt", "a") as log:
        log.write(str(response_dict) + "\n")

    # curl 'https://opac.nblib.cn/api/tcc-open-platform/open-api/service/barcode/currentloan' \
    # -H 'ACCESS-TOKEN: 12345678' \
    # -H 'Accept: application/json, text/plain, */*' \
    # -H 'Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6' \
    # -H 'Connection: keep-alive' \
    # -H 'Content-Type: application/json;charset=UTF-8' \
    # -H 'DNT: 1' \
    # -H 'OPAC-TOKEN: 12345678' \
    # -H 'Origin: https://opac.nblib.cn' \
    # -H 'Sec-Fetch-Dest: empty' \
    # -H 'Sec-Fetch-Mode: cors' \
    # -H 'Sec-Fetch-Site: same-origin' \
    # -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' \
    # -H 'sec-ch-ua: "Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "Windows"' \
    # --data-raw '{"orgId":"623217618121138176","rdid":""}' \
    # --compressed

    headers = {
        "ACCESS-TOKEN": f"{current_access_token}",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,ja-JP;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "DNT": "1",
        "OPAC-TOKEN": f"{current_opac_token}",
        "Origin": "https://opac.nblib.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    json_data = {
        "orgId": "623217618121138176",
        "rdid": f"{current_user_id}",
    }

    response = requests.post(
        "https://opac.nblib.cn/api/tcc-open-platform/open-api/service/barcode/currentloan",
        headers=headers,
        json=json_data,
    )

    response_dict = response.json()
    print(response_dict)
    with open("log.txt", "a") as log:
        log.write(str(response_dict) + "\n")

    nblib_user_list = []

    if "loanlist" in response_dict["data"]:
        nblib_user_list.append(
            f"宁波图书馆({str(current_user_id)[-4:]}):{len(response_dict['data']['loanlist']):02d}本"
        )
        for book in response_dict["data"]["loanlist"]:
            nblib_user_list.append(
                f"{book['returndate'][:10]} {book['title'][:16]} (宁波图书馆已续借{book['renewcount']}次:{current_user_name})"
            )
        # {"code":200,"data":{"..."},"desc":"操作成功"}

    else:
        # print(f"{current_user_id:010d}在宁波图书馆当前借阅00本。")
        nblib_user_list.append(f"宁波图书馆({str(current_user_id)[-4:]}):无借阅")

    return nblib_user_list
