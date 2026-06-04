import hashlib
import random

acceptedchars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ `~!@#$%^&*()-_=+[{]}\\|;:\'\",<.>/?'
char_set = {char: index for index, char in enumerate(acceptedchars)}
reverse_char_set = {index: char for index, char in enumerate(acceptedchars)}


def encrypt(msg=None, key=None, debug=False, fluff_seed=None) -> str:

    if key is None or msg is None:
        raise SyntaxError(f"encrypt() requires two arguments, got encrypt({msg}, {key}{', debug=True' if debug else ''})\nSyntax: encrypt(message, key, [debug=True], [fluff_seed=<str>])")

    if debug:
        print(f"| Arguments\nMessage: {msg}\nKey: {key}\nDebug: {debug}\nFluff Seed: {fluff_seed}")

    estring = ''
    for shift, ch in enumerate(msg):
        seedmaterial = f'{key}:{shift}'.encode()
        shiftkey = hashlib.sha256(seedmaterial).hexdigest()

        if debug:
            print(f'| Seed\nMaterial: {seedmaterial}\nHash: {shiftkey}')

        random.seed(shiftkey)
        temp_char_list = list(char_set.keys())
        random.shuffle(temp_char_list)
        token = ''.join(temp_char_list)
        encrypted_char = token[char_set[ch]]
        estring += encrypted_char

        if debug:
            print(f'| Encrypt\nToken: {token}\n{ch} -> {encrypted_char}\nUpdated Encrypted String: {estring}\n')

    if fluff_seed is None:
        fluff_seed = key[:(len(key)//2)][::-1] + key[(len(key)//2):][::-1]

    fluff_hash = hashlib.sha256(fluff_seed.encode()).hexdigest()
    random.seed(key + fluff_hash)
    fluff_rand1, fluff_rand2 = random.randint(5, 10), random.randint(5, 10)
    temp_char_list = list(char_set.keys())
    random.shuffle(temp_char_list)
    fluff_front = ''.join(temp_char_list[:fluff_rand1][::-1])
    fluff_back = ''.join(temp_char_list[-fluff_rand2:][::-1])

    if debug:
        print(f'| Fluff\nSeed: {fluff_seed}\nHash: {fluff_hash}\nRandInt 1: {fluff_rand1}\nRandInt 2: {fluff_rand2}\nFront: {fluff_front}\nBack: {fluff_back}\n')

    return fluff_front + estring + fluff_back


def decrypt(estring=None, key=None, debug=False, fluff_seed=None) -> str:

    if debug:
        print(f"| Arguments\nEncrypted String: {estring}\nKey: {key}\nDebug: {debug}\nFluff Seed: {fluff_seed}\n")

    if fluff_seed is None:
        fluff_seed = key[:(len(key)//2)][::-1] + key[(len(key)//2):][::-1]

    fluff_hash = hashlib.sha256(fluff_seed.encode()).hexdigest()
    random.seed(key + fluff_hash)
    fluff_rand1, fluff_rand2 = random.randint(5, 10), random.randint(5, 10)
    estring = estring[fluff_rand1:-(fluff_rand2)]

    if debug:
        print(f'| Fluff\nRand 1: {fluff_rand1}\nRand 2: {fluff_rand2}\nExtracted String: {estring}')

    msg = ''
    for shift, ch in enumerate(estring):
        seedmaterial = f'{key}:{shift}'.encode()
        shiftkey = hashlib.sha256(seedmaterial).hexdigest()
        if debug:
            print(f'| Seed\nMaterial: {seedmaterial}\nHash: {shiftkey}')
        random.seed(shiftkey)
        temp_char_list = list(char_set.keys())
        random.shuffle(temp_char_list)
        token = ''.join(temp_char_list)
        current_char = token.index(ch)
        decrypted_char = reverse_char_set[current_char]
        msg += reverse_char_set[token.index(ch)]
        if debug:
            print(f'| Decrypt\nToken: {token}\n{current_char} -> {decrypted_char}\nUpdated Decrypted String: {estring}\n')
    return msg