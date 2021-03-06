import os
import numpy as np
import dcimage
import dcutils

import PIL
import dcutils
import dcimage

import argparse

examples = """
Examples:
    python dcstego.py -e -h image.bmp -k key.txt -o newimage2.bmp
    dcstego.py -d -h newimage2.bmp -k key.txt -o Hidden.bmp
    """

parser = argparse.ArgumentParser(description='Decode/Encode a hidden image in an image.',
                                 epilog=examples,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-e', '--encode', action='store_true',default=False, help='Encode a hidden image in an image.')
parser.add_argument('-d', '--decode', action='store_true',default=False, help='Decode a hidden image in an image.')
parser.add_argument('-k', '--key', help='The key file to use.')
parser.add_argument('-i', '--hidden', help='The hidden image to use / decode.')
parser.add_argument('-c', '--cover', help='The cover image to use.')
parser.add_argument('-o', '--output', help='The output image name.')
parser

def write_key(key):
    f = open('key.txt', 'wb')
    f.write(key)
    print("key written to file:", f.name)
    f.close()

def read_key(filename):
    f = open(filename, 'rb')
    key = f.read()
    f.close()
    return key

def check_args(args):
    if args.encode and args.decode:
        print("Error: cannot encode and decode at the same time.")
        exit(1)
    if not args.encode and not args.decode:
        print("Error: must encode or decode.")
        exit(1)
    if args.encode and not args.cover:
        print("Error: must specify a cover image.")
        exit(1)
    if args.encode and not args.hidden:
        print("Error: must specify a hidden image.")
        exit(1)
    if args.decode and not args.key:
        print("Error: must specify a key.")
        exit(1)
    if args.decode and not args.hidden:
        print("Error: must specify a hidden image.")
        exit(1)
    if args.cover and not os.path.isfile(args.cover):
        print("Error: cover image does not exist.")
        exit(1)
    if args.hidden and not os.path.isfile(args.hidden):
        print("Error: hidden image does not exist.")
        exit(1)
    if args.key and not os.path.isfile(args.key):
        print("Error: key file does not exist.")
        exit(1)
    if args.output and os.path.isfile(args.output):
        print("Error: output file already exists.")
        exit(1)
    if args.output and not args.output.endswith('.bmp'):
        print("Error: output file must be a .bmp file.")
        exit(1)
    if args.cover and not args.cover.endswith('.bmp'):
        print("Error: cover file must be a .bmp file.")
        exit(1)
    if args.hidden and not args.hidden.endswith('.bmp'):
        print("Error: hidden file must be a .bmp file.")
        exit(1)
    if args.key and not args.key.endswith('.txt'):
        print("Error: key file must be a .txt file.")
        exit(1)


def main(args):
    #load image
    cover = dcimage.load_image(args.cover)
    #load hidden image
    hidden = dcimage.load_hidden_image(args.hidden)
    # encrypt the string
    ciphertext, key = dcutils.encrypt(hidden)
    #write key to file
    write_key(key)
    # encode string to binary
    binstr = dcutils.str2bin(ciphertext)
    # get length of binary string
    l = dcutils.length(binstr)
    # print(l)
    # combine length and binary string
    binstr = l + binstr
    # encode binary to image
    print("encoding")
    img = dcutils.encode_image(cover, binstr)

    # save image
    print("Saving image")
    if args.output:
        dcimage.save_image(str(args.output), img)
        print("Saved image to :", args.output)
    else:
        dcimage.save_image('output.bmp', img)
        print("Saved image to :", 'output.bmp')

def main2(args):
    #load image
    cover = dcimage.load_image(args.hidden)
    #load key
    key = read_key(args.key)
    #decode image
    print("decoding")
    binstr = dcutils.decode_image(cover)
    #decode binary to string
    plaintext = dcutils.bin2str(binstr)
    #dehexlify
    plaintext = bytes.fromhex(plaintext)
    #decrypt the string
    print("decrypting")
    plaintext = dcutils.decrypt(plaintext, key)
    with open(args.output, 'wb') as f:
        f.write(plaintext)
    print("Saved image to :", f.name)

if __name__ == '__main__':
    #read flags
    args = parser.parse_args()
    if args.encode:
        check_args(args)
        main(args)
    elif args.decode:
        check_args(args)
        main2(args)
    else:
        print("Please specify an action.")
        exit()
