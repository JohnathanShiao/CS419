#!/usr/bin/python3
import sys, os

def decrypt(kfd, cfd, pfd):
    ciphertext = []
    keyfile = []
    keyfile_length = 0
    x = 0

    curr = cfd.read(1)
    while curr:
        ciphertext.append(curr)
        curr = cfd.read(1)

    curr = kfd.read(1)
    if curr == b'':
        #if empty, flag to return only ciphertext
        x=1
    else:
        while curr:
            keyfile.append(curr)
            curr = kfd.read(1)
        keyfile_length = len(keyfile)
        
    keyfile_length = len(keyfile)
    i=0
    for byte in range(len(ciphertext)):
        if keyfile and len(keyfile) == i:
            i = 0
        if x:
            c = ord(ciphertext[byte])
        else:
            c = ord(ciphertext[byte]) - ord(keyfile[i])
            while c < 0:
                c+=256
        pfd.write(int.to_bytes(c,byteorder=sys.byteorder,length=1))
        i+=1
    return keyfile_length

def main():
    key = sys.argv[1]
    cipher = sys.argv[2]
    plain = sys.argv[3]
    if len(sys.argv) < 4:
        print("Error: missing arguments, expecting: 'vencrypt keyfile plaintext ciphertext'")
        return
    try:
        kfd = open(key,"rb")
    except:
        print("Error: could not open {}".format(key))
        return
    try:
        cfd = open(cipher,"rb")
    except:
        print("Error: could not open {}".format(cipher))
        return
    if os.path.exists(plain):
        os.remove(plain)
    pfd = open(plain,"wb")
    decrypt(kfd,cfd,pfd)
    kfd.close()
    pfd.close()
    cfd.close()
    return

if __name__ == "__main__":
    main()