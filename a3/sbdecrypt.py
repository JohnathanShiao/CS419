#!/usr/bin/python3
import sys, os, copy

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

def unpad(block):
    i = block[15]
    temp_block = block[:(16-i)]
    # print("removing padding, start offset={}: value={}".format(16-i,i))
    return temp_block

def swap(block, keystream):
    for i in range(15,-1,-1):
        first = keystream[i] & 0xf
        second = (keystream[i]>>4) & 0xf
        block[first:first+1], block[second:second+1] = block[second:second+1], block[first:first+1]
        # print("{}: swapping ({},{})".format(i,first,second))
    return block

def decrypt(password, pfd, cfd):
    #use password to make seed
    seed = sdbm(password)
    first_time = 1
    #use seed to generate keystream
    stream_num = seed
    init_vec = bytearray()
    
    #read cipher 16 bytes
    curr = cfd.read(16)
    prev_cipher = copy.deepcopy(curr)
    while curr:
        key_block= bytearray()

        # print("prev_cipher: {}".format(''.join('{:02x} '.format(x) for x in prev_cipher)))

        if first_time:
            #generate initialization vector
            for i in range(0,16):
                stream_num = generate(stream_num)
                init_vec.extend(int.to_bytes(stream_num,byteorder=sys.byteorder,length=1))
        
        #read 16 bytes of keystream
        for i in range(0,16):
            stream_num = generate(stream_num)
            key_block.extend(int.to_bytes(stream_num,byteorder=sys.byteorder,length=1))

        
        # print("encrypted block before shuffle: {}".format(''.join('{:02x} '.format(x) for x in curr)))
        # print("keystream: {}".format(''.join('{:02x} '.format(x) for x in key_block)))
        #xor ciphertext with keystream
        p = myxor(curr,key_block)

        # print("after xor with keystream: {}".format(''.join('{:02x} '.format(x) for x in p)))
        #swap the result of the xor
        swapped = swap(p,key_block)

        # print("CBC: {}".format(''.join('{:02x} '.format(x) for x in prev_cipher)))
        # print("plaintext before xor with CBC: {}".format(''.join('{:02x} '.format(x) for x in swapped)))
        #xor with previous block or init vector
        if first_time:
            plain = myxor(swapped,init_vec)
            first_time = 0
        else:
            plain = myxor(swapped,prev_cipher)
        # print("after plaintext xor CBC: {}".format(''.join('{:02x} '.format(x) for x in plain)))
        # print()

        #remove padding if last block
        next = cfd.read(16)
        if next == b'':
            #if last block, unpad
            plain = unpad(plain)
        #write
        pfd.write(plain)
        prev_cipher = copy.deepcopy(curr)
        curr = next
    
    return seed

def main():
    password = sys.argv[1]
    cipher = sys.argv[2]
    plain = sys.argv[3]
    if len(sys.argv) < 4:
        print("Error: missing arguments, expecting: 'vencrypt keyfile plaintext ciphertext'")
        return
    if password is None:
        print("Error: no password given")
        return
    try:
        cfd = open(cipher,"rb")
    except:
        print("Error: could not open {}".format(cipher))
        return
    if os.path.exists(plain):
        os.remove(plain)
    pfd = open(plain,"wb")
    x = decrypt(password,pfd,cfd)
    print("ciphertextfile={}, plaintextfile={} password={}".format(cipher, plain, password))
    pfd.close()
    cfd.close()
    return

if __name__ == "__main__":
    main()