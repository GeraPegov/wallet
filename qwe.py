import random 
import hashlib

num = str(random.random())
m = hashlib.new('shake_256')
m.update(num.encode())
hash = m.hexdigest(5)
print(hash)
