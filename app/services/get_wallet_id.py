import hashlib
import random


class CreateWalletHash:
    def hash(self):
        num = str(random.random())
        m = hashlib.new("shake_256")
        m.update(num.encode())
        hash = m.hexdigest(5)
        return hash
