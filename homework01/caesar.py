import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    for ch in plainText:
        if ch.isalpha():
            stayInAlphabet = ord(ch) + shift 
            if stayInAlphabet > ord('z'):
                stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
        cipherText = ""
        cipherText += finalLetter

        print ("Your ciphertext is: ", cipherText)

        return cipherText
    
    


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    for ch in plainText:
        if ch.isalpha():
            stayInAlphabet = ord(ch) - shift 
            if stayInAlphabet < ord('z'):
                stayInAlphabet += 26
            finalLetter = chr(stayInAlphabet)
        plainText = ""
        plainrText -= finalLetter

        print ("Your ciphertext is: ", plainText)

        return plainText


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
