#!/usr/bin/python3
import sys, os

def generate(num):
    a = 1103515245
    c = 12345
    m = 256
    return (a*num + c)%m

def sdbm(password):
    hash = 0
    for char in password:
        i = ord(char)
        hash = i + (hash << 6 ) + (hash << 16) - hash
    return hash

def myxor(bytes1,bytes2):
    return bytes([_a ^ _b for _a, _b in zip(bytes1,bytes2)])

def encrypt(password, pfd, cfd):
    #use password to make seed
    seed = sdbm(password)
    
    #use seed to generate keystream
    stream_num = seed
    
    curr = pfd.read(1)
    while curr:
        stream_num = generate(stream_num)
        #exclusive or each number to each char
        c = myxor(curr,int.to_bytes(stream_num,byteorder=sys.byteorder,length=1))
        cfd.write(c)
        curr = pfd.read(1)
    
    return seed

def main():
    password = sys.argv[1]
    plain = sys.argv[2]
    cipher = sys.argv[3]
    if len(sys.argv) < 4:
        print("Error: missing arguments, expecting: 'vencrypt keyfile plaintext ciphertext'")
        return
    if password is None:
        print("Error: no password given")
        return
    try:
        pfd = open(plain,"rb")
    except:
        print("Error: could not open {}".format(plain))
        return
    if os.path.exists(cipher):
        os.remove(cipher)
    cfd = open(cipher,"wb")
    x = encrypt(password,pfd,cfd)
    print("password={}, seed={}".format(password, x))
    pfd.close()
    cfd.close()
    return

if __name__ == "__main__":
    main()