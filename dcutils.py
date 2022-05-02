import PIL
import numpy as np
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

#load file
def load_file(path):
    with open(path, 'rb') as f:
        data = f.read()
    return data

def decrypt(ciphertext, key):
    #generate key
    # key = b'\x1d\xd7\xccl\xfe\xfb\xa4_\xaac\x0e\r\xea\xd9\xe6`'
    # print(key)
    cipher = DES3.new(key, DES3.MODE_CBC, b'\xb3\xee#\x97\x99u\xde\xb9')
    plaintext = cipher.decrypt(ciphertext)
    # print(cipher.iv)
    return plaintext

def encrypt(plaintext):
    #generate key
    key = get_random_bytes(16)
    # print(key)
    plaintext = pad(plaintext, DES3.block_size)
    cipher = DES3.new(key, DES3.MODE_CBC, iv=b'\xb3\xee#\x97\x99u\xde\xb9')
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext.hex(), key


def str2bin(string):
    # convert string to binary
    binstr = ''
    for char in string:
        binstr += bin(ord(char))[2:].zfill(8)
    return binstr

def bin2str(binstr):
    # convert binary to string
    string = ''
    for i in range(0, len(binstr), 8):
        string += chr(int(binstr[i:i+8], 2))
    return string

def length(binstr):
    l = len(binstr)
    #convert to 24 didget binary
    l = bin(l)[2:].zfill(24)
    # print(l)
    #if l is greater than 24, then return error
    if len(l) > 24:
        raise Exception('Length of binary string is greater than 24')
    return l

def encode_image(img, binstr):
    # encode binary to image using least significant bit
    # img: numpy array
    # binstr: binary string
    # return: numpy array
    for i in img:
        for j in i:
            for k in range(3):
                try:
                    bine = np.binary_repr(j[k])
                    # turn binary string to list
                    bine = list(bine)
                    bine[-1] = binstr[0]
                    binstr = binstr[1:]
                    # turn list to binary string
                    bine = ''.join(bine)
                    j[k] = int(bine, 2)
                    # print("values left: " + str(len(binstr)))
                except IndexError:
                    return img
                    
    return img

def decode_image(img):
    # decode binary from image using least significant bit
    # img: numpy array
    # return: binary string
    binstr = ''
    l = ''
    for i in img:
        for j in i:
            for k in range(3):
                if l == '':
                    binstr += np.binary_repr(j[k])[-1]
                    if len(binstr) == 24:
                        l = int(binstr[0:24], 2)
                        binstr = ''
                else:
                    binstr += np.binary_repr(j[k])[-1]
                    if len(binstr) == l:
                        return binstr