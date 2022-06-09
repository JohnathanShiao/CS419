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
    return bytearray([_a ^ _b for _a, _b in zip(bytes1,bytes2)])

def pad(block):
    i = 16 - len(block)
    for x in range(0,i):
        block+= bytes([i])
    return block

def swap(block, keystream):
    for i in range(0,16):
        first = keystream[i] & 0xf
        second = (keystream[i]>>4) & 0xf
        block[first:first+1], block[second:second+1] = block[second:second+1], block[first:first+1]
        # print("{}: swapping ({},{})".format(i,first,second))
    return block

def encrypt(password, pfd, cfd):
    #use password to make seed
    seed = sdbm(password)
    first_time = 1
    #use seed to generate keystream
    stream_num = seed
    init_vec = bytearray()
    
    prev_cipher = []
    #read plaintext 16 bytes
    curr = pfd.read(16)

    while curr:
        key_block= bytearray()
        #check if last block, add padding
        if len(curr) < 16:
            curr = pad(curr)
        
        #xor the data with previous block
        if first_time:
            #generate initialization vector
            for i in range(0,16):
                stream_num = generate(stream_num)
                init_vec.extend(int.to_bytes(stream_num,byteorder=sys.byteorder,length=1))
            first_time = 0
            c = myxor(curr,init_vec)
        else:
            c = myxor(curr,prev_cipher)

        #read 16 bytes of keystream
        for i in range(0,16):
            stream_num = generate(stream_num)
            key_block.extend(int.to_bytes(stream_num,byteorder=sys.byteorder,length=1))

        # print("before shuffle: {}".format(''.join('{:02x} '.format(x) for x in c)))
        # print("keystream: {}".format(''.join('{:02x} '.format(x) for x in key_block)))
        #swap 16 pairs of bytes
        swapped = swap(c,key_block)

        #xor with keystream
        cipher = myxor(swapped,key_block)

        # print("after shuffle: {}".format(''.join('{:02x} '.format(x) for x in swapped)))
        # print("after xor with keystream: {}".format(''.join('{:02x} '.format(x) for x in cipher)))
        # print()
        #write
        cfd.write(cipher)
        prev_cipher = cipher

        curr = pfd.read(16)
    
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
    print("ciphertextfile={}, plaintextfile={} password={}".format(cipher, plain, password))
    pfd.close()
    cfd.close()
    return

if __name__ == "__main__":
    main()