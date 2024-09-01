import string

def textstrip(filename):
    '''This takes the file and converts it to a string with all the spaces and other
    special characters removed. What remains is only the lower case letters,
    retain only the lowercase letters!
    '''
    with open(filename, 'r') as file:
        text = file.read()
        text = text.lower()
        text = text.replace(" ", "")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.translate(str.maketrans('', '', string.digits))
    return text

def letter_distribution(s):
    '''Consider the string s which comprises of only lowercase letters. Count
    the number of occurrences of each letter and return a dictionary'''
    letter_dict = {}
    for letter in s:
        if letter in letter_dict:
            letter_dict[letter] += 1
        else:
            letter_dict[letter] = 1
    return letter_dict

def substitution_encrypt(s, d):
    '''encrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    encrypted_text = ""
    for letter in s:
        if letter in d:
            encrypted_text += d[letter]
        else:
            encrypted_text += letter
    return encrypted_text

def substitution_decrypt(s, d):
    '''decrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    decrypted_text = ""
    reverse_d = {v: k for k, v in d.items()}
    for letter in s:
        decrypted_text += reverse_d.get(letter, letter)
    return decrypted_text

def cryptanalyse_substitution(s):
    '''Given that the string s is given to us and it is known that it was
    encrypted using some substitution cipher, predict the d'''
    # Frequency Analysis of the letters
    letter_dict = letter_distribution(s)
    sorted_letter_dict = sorted(letter_dict.items(), key=lambda x: x[1], reverse=True)
    # Frequency Analysis of the English Language
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    english_dict = {}
    for i in range(26):
        english_dict[english_letter_freq[i]] = sorted_letter_dict[i][0]
    return english_dict

def vigenere_encrypt(s,password):
    '''Encrypt the string s using the Vigenere cipher with the given password.
    Return the resulting string'''
    encrypted_text = ""
    password_length = len(password)
    for i in range(len(s)):
        shift = (ord(password[i % password_length]) - 97) % 26
        encrypted_text += chr((ord(s[i]) - 97 + shift) % 26 + 97)
    return encrypted_text

def vigenere_decrypt(s,password):
    '''Decrypt the string s using the Vigenere cipher with the given password.
    Return the resulting string'''
    decrypted_text = ""
    password_length = len(password)
    for i in range(len(s)):
        shift = (ord(password[i % password_length]) - 97) % 26  # Adjusted shift calculation
        decrypted_text += chr((ord(s[i]) - 97 - shift + 26) % 26 + 97)  # Corrected modulo operation to handle alphabetic range
    return decrypted_text

def rotate_compare(s,r):
    '''This rotates the string s by r places and compares s(0) with s(r) and 
    returns the number of collisions'''
    collisions = 0
    for i in range(len(s)):
        if s[i] == s[(i+r) % len(s)]:
            collisions += 1
    return collisions

def cryptanalyse_vigenere_afterlength(s,k):
    '''Given the string s which is known to be vigenere encrypted with a
    password of length k, find out what is the password'''
    # Frequency Analysis of the letters
    letter_dict = letter_distribution(s)
    sorted_letter_dict = sorted(letter_dict.items(), key=lambda x: x[1], reverse=True)
    # Frequency Analysis of the English Language
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    english_dict = {}
    for i in range(26):
        english_dict[english_letter_freq[i]] = sorted_letter_dict[i][0]
    password = ""
    for i in range(k):
        password += english_dict[english_letter_freq[i]]
    return password

def cryptanalyse_vigenere_findlength(s):
    '''Given the string s which is known to be vigenere encrypted, find out what
    is the length of the password'''
    # Frequency Analysis of the letters
    letter_dict = letter_distribution(s)
    sorted_letter_dict = sorted(letter_dict.items(), key=lambda x: x[1], reverse=True)
    # Frequency Analysis of the English Language
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    english_dict = {}
    for i in range(26):
        english_dict[english_letter_freq[i]] = sorted_letter_dict[i][0]
    # Find the length of the password
    password_length = 0
    for i in range(26):
        if english_dict[english_letter_freq[i]] == 'e':
            password_length = i
            break
    return password_length

def cryptanalyse_vigenere(s):
    '''Given the string s which is known to be vigenere encrypted, output the password and decrypted string'''
    password_length = cryptanalyse_vigenere_findlength(s)
    password = cryptanalyse_vigenere_afterlength(s,password_length)
    decrypted_text = vigenere_decrypt(s,password)
    return password, decrypted_text

def main():
    print("Choose an operation:")
    print("1. Substitution Cipher Encryption")
    print("2. Substitution Cipher Decryption")
    print("3. Vigenère Cipher Encryption")
    print("4. Vigenère Cipher Decryption")
    print("5. Cryptanalysis of Substitution Cipher")
    print("6. Cryptanalysis of Vigenère Cipher")
    
    choice = int(input("Enter your choice (1-6): "))
    filename = input("Enter the filename with text: ")
    text = textstrip(filename)

    if choice == 1:
        d = {}
        print("Enter the substitution dictionary (26 letters):")
        for i in range(26):
            key = chr(97 + i)
            value = input(f"Substitute {key} with: ")
            d[key] = value
        encrypted = substitution_encrypt(text, d)
        print("Encrypted string:", encrypted)
    
    elif choice == 2:
        d = {}
        print("Enter the substitution dictionary (26 letters):")
        for i in range(26):
            key = chr(97 + i)
            value = input(f"Substitute {key} with: ")
            d[key] = value
        decrypted = substitution_decrypt(text, d)
        print("Decrypted string:", decrypted)
    
    elif choice == 3:
        password = input("Enter the password: ")
        encrypted = vigenere_encrypt(text, password)
        print("Encrypted string:", encrypted)
    
    elif choice == 4:
        password = input("Enter the password: ")
        decrypted = vigenere_decrypt(text, password)
        print("Decrypted string:", decrypted)
    
    elif choice == 5:
        predicted_dict = cryptanalyse_substitution(text)
        print("Predicted substitution dictionary:")
        for key, value in predicted_dict.items():
            print(f"{key} -> {value}")
    
    elif choice == 6:
        password, decrypted_text = cryptanalyse_vigenere(text)
        print("Predicted password:", password)
        print("Decrypted string:", decrypted_text)
    
    else:
        print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
