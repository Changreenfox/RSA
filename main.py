# Final project
# Chandler Fox
# Phong Quach
# Dr.P
# MAS2002
# 12/13/19

def gcd(a, b):
    # Calculates the GCD of 2 numbers
    if b == 0:
        return a
    return gcd(b, a % b)


def dioph(a, b):
    # Solves for a linear diophantine equation
    if a % b == 0:
        return 0, 1
    x, y = dioph(b, a % b)
    return y, x-(y*(a//b))


def prime_factors(n):
    # Prime Factors decomposition
    i = 2
    Factors = []
    while i*i <= n:
        if n % i == 0:
            Factors += [i]
            n //= i
        else:
            i += 1
    return Factors + [n]


def phi(n):
    # Euler's function for calculating Phi
    Factors = prime_factors(n)
    UniqueFactors = set(Factors)
    Result = 1
    for p in UniqueFactors:
        k = Factors.count(p)
        Result *= (p**k-p**(k-1))
    return Result


def power_mod_m(a, k, m):
    # Calculates the mod of a^k using Successive Squaring
    b = 1
    while k >= 1:
        if k % 2 == 1:
            b = (a*b) % m
        a = a**2 % m
        k //= 2
    return b


# Finds what value x works for x^k = b(mod m) if any
def kth_root_mod_m(k, b, m):
    x = phi(m)
    # If the gcd isn't 1 for both of these, this test wouldn't output the correct answer
    if gcd(b, m) != 1 or gcd(k, x) != 1:
        return
    # The process involves solving the diophantine equation for k and Phi(m). If u is negative, increment it by Phi(m)
    u, v = dioph(k, x)
    if u < 0:
        u += x
    # This is where we finally calculate b^u(mod m) = x, and output the results
    return u, power_mod_m(b, u, m)


def RSA(encryption=True):
    if encryption:
        # **************************Encryption**************************
        # 1 - Acquire the name and get M and K from the file. Handle errors with a try, except segment
        print("Please type in the name of the file with k and m.")
        FileName = input("Type publickey.txt if need to use the default :\n")
        try:
            with open(FileName) as File:
                S = File.readlines()
        except IOError:
            print("That File does not exist")
            return

        Test = [Line for Line in S if '#' not in Line and Line != "\n"]
        M = Test[0]
        K = Test[1]
        print("The Modulus is", M, "and the Auxiliary Key is", K)

        # Ask to receive the Text to be encrypted
        print("\nPlease type in the name of the file to encrypt.")
        TextName = input("Type plaintext.txt if you need to default\n")
        try:
            with open(TextName) as File:
                S = File.read()
        except IOError:
            print("That File does not exist")
            return

        # The Actual Encryption.
        print(S)
        # This is where we convert the plaintext into integers and place 0 in the list to
        # make sure that it matches the length of the chunking size
        Cipher = []
        Chunk = len(M)-1
        # Convert the chars to int values and store them in a string
        for Char in S:
            String = str(ord(Char))
            String = String.zfill(3)
            Cipher.append(String)
        # Now that we're out of characters, pad the last chunk
        padding = len(Cipher) % Chunk
        for i in range(padding):
            Cipher.append('0')
        CipherText = "".join(Cipher)

        # This is where we put the chunks together and raises each one to the power of K and then divide by the modulo M
        Encryption = []
        chunk_count = len(CipherText) // Chunk
        # For each chunk, pull out the whole chunk and convert to an int
        for i in range(0, chunk_count):
            Encryption.append(int(CipherText[i*Chunk: (i+1)*Chunk]))
        EncryptedText = [power_mod_m(C, int(K), int(M)) for C in Encryption]

        # Ask where to store the encrypted message
        FileName = input("\n\n\nWhere would you like to store this Cipher?\nThe default name is cipher.txt\n")

        with open(FileName, "w+") as File:
            for Line in range(0, len(EncryptedText)):
                File.write(str(EncryptedText[Line]) + "\n")

        # Signifies that it has been encrypted
        print("Your Message has been Encrypted")
        return
    # **************************Decryption*************************** #
    else:
        # Ask for a file name to get M, Phi(m), and K
        print("Please type in the name of the file with the public, private, and Auxiliary keys M, Phi(M), k.")
        FileName = input("Type the default privatekey.txt if there is no additional file:\n")
        try:
            with open(FileName) as File:
                S = File.readlines()
        except IOError:
            print("That File does not exist")
            return

        # Interpret the File
        Test = [Line for Line in S if '#' not in Line and Line != "\n"]
        M = int(Test[0])
        Chunk = len(str(M))-1
        P = int(Test[1])
        K = int(Test[2])
        print("The Modulus is", M, "\nThe private Key is", P, "\nand the Auxiliary Key is", K, "\n")

        # Ask for a file to Decrypt
        print("\nPlease type in the name of the file to Decrypt.")
        TextName = input("Type cipher.txt if you need to default:\n")
        try:
            with open(TextName) as File:
                EncryptedText = File.readlines()
        except IOError:
            print("That File does not exist")
            return

        # The actual Decryption

        # This is where we find the inverse of k through the Diophantine equation, take the inverse, and raise each
        # given value by U and modding M, making sure to pad out any 0's that fell off when converting to integers
        # during encryption.
        U, V = dioph(K, P)
        if U < 0:
            U = U + P
        DecryptedText = []

        for Line in EncryptedText:
            String = str(power_mod_m(int(Line), U, M))
            String = String.zfill(Chunk)
            DecryptedText.append(String)

        Decryption = "".join(Number for Number in DecryptedText)

        # Turning the giant number into a bunch of little numbers less than 127 (The ASCII table) and changing them back
        # into letters to receive the message
        PlainText = []
        i = 0
        while i < len(Decryption)-3:
            Num = int(Decryption[i:i+3])
            if Num > 127:
                Num = int(Decryption[i: i+2])
                i += 2
            else:
                i += 3

            # If there are trailing Zeroes, this will catch them
            if Num:
                PlainText.append(Num)

        Text = "".join(chr(Character) for Character in PlainText)
        print(Text)

        # Store the Decoded message in a given file
        FileName = input("\n\n\nWhere Would you like to store this?\nplaintext.txt is the default option.\n")
        with open(FileName, "w+") as File:
            File.write(Text)
            print("The code has been successfully decoded")

    
# Main
def main():
    RSA()
    RSA(False)


# Dunder
if __name__ == "__main__":
    main()
