print('By 348829605\nAccepted characters: 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ `~!@#$%^&*()-_=+[{]}\\|;:\'\",<.>/?')
import random
import hashlib
import pyperclip
char = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29, 'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35, 'A': 36, 'B': 37, 'C': 38, 'D': 39, 'E': 40, 'F': 41, 'G': 42, 'H': 43, 'I': 44, 'J': 45, 'K': 46, 'L': 47, 'M': 48, 'N': 49, 'O': 50, 'P': 51, 'Q': 52, 'R': 53, 'S': 54, 'T': 55, 'U': 56, 'V': 57, 'W': 58, 'X': 59, 'Y': 60, 'Z': 61, ' ': 62, '`': 63, '~': 64, '!': 65, '@': 66, '#': 67, '$': 68, '%': 69, '^': 70, '&': 71, '*': 72, '(': 73, ')': 74, '-': 75, '_': 76, '=': 77, '+': 78, '[': 79, '{': 80, ']': 81, '}': 82, '\\': 83, '|': 84, ';': 85, ':': 86, '\'': 87, '\"': 88, ',': 89, '<': 90, '.': 91, '>': 92, '/': 93, '?': 94}


def encrypt(msg, key):
    random.seed(key)
    temp = list(char.keys()); random.shuffle(temp)
    token, estring = ''.join(temp), ''
    for shift, ch in enumerate(msg):
        seedmaterial = f'{key}:{shift}'.encode()
        shiftkey = hashlib.sha256(seedmaterial).hexdigest()
        random.seed(shiftkey)
        temp = list(char.keys()); random.shuffle(temp)
        token = ''.join(temp)
        estring += token[char[ch]]
    random.seed(key+'supersecretphrase')
    temp = list(char.keys()); random.shuffle(temp)
    return ''.join(temp[:random.randint(1, 7)][::-1]) + estring

def decrypt(estring, key):
    random.seed(key+'supersecretphrase')
    temp = list(char.keys())
    random.shuffle(temp)
    prefixlen = random.randint(1, 7)
    estring = estring[prefixlen:]
    msg = ''
    reversechar = {v: k for k, v in char.items()}
    for shift, ch in enumerate(estring):
        seedmaterial = f'{key}:{shift}'.encode()
        shiftkey = hashlib.sha256(seedmaterial).hexdigest()
        random.seed(shiftkey)
        temp = list(char.keys()); random.shuffle(temp)
        token = ''.join(temp)
        msg += reversechar[token.index(ch)]
    return msg


def nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('Cannot be blank\n')
while True:
    choice = input('[E]ncrypt\n[D]ecrypt\n[Q]uit\n> ').strip().lower()
    if choice == 'q':
        break
    if choice not in {'e', 'd'}:
        print('Invalid selection\n')
        continue
    text = nonempty('Message:\n> ')
    key = nonempty('Key:\n> ')
    if choice == 'e':
        result = encrypt(text, key)
        print(f'\nEncrypted message: {result}\n(Copied to clipboard)\n')
        pyperclip.copy(result)
    else:
        result = decrypt(text, key)
        print(f'\nDecrypted message: {result}\n(Copied to clipboard)\n')
        pyperclip.copy(result)
