#!/usr/bin/python3
import hashlib, sys, time, itertools, math

count = 0
h = hashlib.sha256()

def hash(str):
    h = hashlib.sha256()
    h.update(str.encode())
    return h.hexdigest()

def find_proof(init_sha, leading, charset):
    return

def leading_zeros(hex_str):
    zeros = 0
    temp = int(hex_str, base=16)
    bits = f'{temp:0>256b}'
    for i in range(0,len(bits)):
        if bits[i] == '1':
            break
        zeros+=1
    return zeros

def main():

    header = sys.argv[1]
    file = sys.argv[2]
    init_sha = hashlib.sha256()
    fail_flag = 0
    #extract data from header
    hfd = open(header,'r')
    header_lines = hfd.readlines()

    for line in header_lines:
        if "Initial" in line:
            header_init = line[13:].strip()
        elif "Proof" in line:
            header_pow = line[14:].strip()
        elif "Hash" in line:
            header_hash = line[5:].strip()
        elif "Leading" in line:
            header_zeros = line[18:].strip()

    # print("INIT:{}\nPROOF:{}\nHASH:{}\nLEADING:{}".format(header_init,header_pow,header_hash,header_zeros))
    #check initial file hashes
    with open(file,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            init_sha.update(byte_block)
    
    if len(header_init) == 0:
        print("ERROR: missing Inital-hash in header")
    elif init_sha.hexdigest() == header_init:
        print("PASSED: initial file hashes match")
    else:
        print("ERROR: initial hashes don't match\n\thash in header:\t{}\n\tfile hash:\t{}".format(header_init,init_sha.hexdigest()))
        fail_flag = 1
    #check leading bits
    num_zeros= leading_zeros(hash(init_sha.hexdigest()+header_pow))
    if num_zeros == int(header_zeros):
        print("PASSED: leading bits is correct")
    else:
        print("ERROR: incorrect leading-bits value: {}, but hash has {}".format(header_zeros,num_zeros))
        fail_flag = 1

    #check pow hash with header
    temp_hash = hash(init_sha.hexdigest()+header_pow)
    if temp_hash == header_hash:
        print("PASSED: pow hash matches Hash header")
    else:
        print("ERROR: pow hash does not match Hash header\n\texpected:\t{}\n\theader has:\t{}".format(temp_hash,header_hash))
        fail_flag = 1

    #print pass fail
    if fail_flag:
        print("fail")
    else:
        print("pass")
    return

if __name__ == "__main__":
    main()