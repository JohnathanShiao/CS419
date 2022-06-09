#!/usr/bin/python3
import sys, os

def encrypt(kfd, pfd, cfd):
    plaintext = []
    keyfile = []
    keyfile_length = 0
    x= 0
    
    curr = pfd.read(1)
    while curr:
        plaintext.append(curr)
        curr = pfd.read(1)

    curr = kfd.read(1)
    if curr == b'':
        #if empty, flag to return only plaintext
        x=1
    else:
        while curr:
            keyfile.append(curr)
            curr = kfd.read(1)
        keyfile_length = len(keyfile)
    i=0
    for byte in range(len(plaintext)):
        if keyfile and len(keyfile) == i:
            i = 0
        if x:
            c = ord(plaintext[byte])%256
        else:
            c = (ord(plaintext[byte]) + ord(keyfile[i]))%256
        cfd.write(int.to_bytes(c,byteorder=sys.byteorder,length=1))
        i+=1
    return keyfile_length

def main():
    key = sys.argv[1]
    plain = sys.argv[2]
    cipher = sys.argv[3]
    if len(sys.argv) < 4:
        print("Error: missing arguments, expecting: 'vencrypt keyfile plaintext ciphertext'")
        return
    try:
        kfd = open(key,"rb")
    except:
        print("Error: could not open {}".format(key))
        return
    try:
        pfd = open(plain,"rb")
    except:
        print("Error: could not open {}".format(plain))
        return
    if os.path.exists(cipher):
        os.remove(cipher)
    cfd = open(cipher,"wb")
    x = encrypt(kfd,pfd,cfd)
    print("keyfile={}, length={}".format(key, x))
    kfd.close()
    pfd.close()
    cfd.close()
    return

if __name__ == "__main__":
    main()