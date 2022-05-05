import hashlib

def compute_hash(tmp, nonce):
    string = tmp + str(nonce)
    return hashlib.sha256(string.encode()).hexdigest()

def compute_nonce(transaction, prev_hash):
    tmp = transaction + prev_hash
    nonce = 1
    cur_hash = compute_hash(tmp, nonce)
    while not cur_hash.startswith('0000'):
        nonce += 1
        cur_hash = compute_hash(tmp, nonce)
    print(nonce)
    print(cur_hash)
    return nonce

if __name__ == "__main__":
    compute_nonce("Shuo", "000036994fc1f2b1f597fef58b93c592954ba26388f6ee5c51ee4b8a328ed176")
