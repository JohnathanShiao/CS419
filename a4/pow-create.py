#!/usr/bin/python3
import hashlib, sys, time, itertools, math

count = 0
h = hashlib.sha256()

def hash(str):
    h = hashlib.sha256()
    h.update(str.encode())
    return h.hexdigest()

def gen_strings(charset):
    m = len(charset)
    for n in itertools.count(0):
        for i in range(m**n):
            yield ''.join([charset[(i//(m**j))%m] for j in range(n)])

def find_proof(init_sha, leading, charset):
    for token in gen_strings(charset):
        # print("after hash: {}".format(hash(init_sha+token)))
        global count
        count+=1
        if leading_zeros(hash(init_sha+token)) >= leading: 
            return token

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

    leading = int(sys.argv[1])
    file = sys.argv[2]
    init_sha = hashlib.sha256()

    print("File: {}".format(file))
    with open(file,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            init_sha.update(byte_block)
    
    print("Initial-hash: {}".format(init_sha.hexdigest()))

    start = time.time()
    work = find_proof(init_sha.hexdigest(),leading,charset='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=')
    end = time.time()

    print("Proof-of-work: {}".format(work))
    print("Hash: {}".format(hash(init_sha.hexdigest()+work)))
    print("Leading-zero-bits: {}".format(leading_zeros(hash(init_sha.hexdigest()+work))))
    print("Iterations: {}".format(count))
    print("Compute-time: {}".format(end-start))
    return

if __name__ == "__main__":
    main()