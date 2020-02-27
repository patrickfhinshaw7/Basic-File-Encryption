
"""      
	This module takes the contents of a file, and encrypts them using three
	different encryption methods and a password. These encrypted contents are then
	written to a new file and stored. These encrypted files can then be decrypted
	by using the password you used to encrypt. The contents of the decrypted files
	will be sent to a new file.
"""


#------------- Encrypting Functions ------------------------------------


def transpose_encrypt(string, n):
    """encrypts a string using 'n' amount of rails.


        args:
            string: A string that will be transposed.
            n: The number of rails the string will be divided into.


        returns: a cipher with all of the rails concatenated together.
        For example, the string 'abcdefghi' with n = 3 will return the cipher
        'adgbehcfi'.
          1  2  3


    """
    
    cipher = ""
    for i in range(n):
        for j in range(i, len(string), n):
            cipher += string[j]
    return cipher
            
def shift_encrypt(message):
    """Encrypts a string by shifting the ASCII codes of characters.


        This function is limited however, and only shifts by 13.


        args:
            message: The string whose characters will be shifted by 13
            ASCII numbers, producing a cipher.


        returns: a cipher created by shifting characters. Only shifts characters
        if they are within the printable ASCII numbers, 32 - 126.


    """
        
    cipher = ""
    alpha = generate_alpha()
    for x in message:
        num = ord(x)
        if x not in alpha:
            cipher += x
        elif num + 13 > 126:
            cipher += chr(31 + num + 13 - 126)
        else:
            cipher += chr(num + 13)


    return cipher


#This function can also be used to decrypt the substitution cipher
def sub_encrypt(message, alpha, key):
    """ Encrypts a string by using a key to switch the characters.


        args:
            message: The string that will be encrypted
            alpha: All of the printable numbers in the ASCII numbers (32-126)
            key: The key created by using the letters of a password to
            specifically rearrange the alphabet, creating a key.


        returns: a string thats been encrypted according to the arrangement of
        the key.


    """
    
    cipher = ""
    for ch in message:
        if ch in alpha:
            i = alpha.find(ch)
            new_ch = key[i]
            cipher += new_ch
        else:
            cipher += ch
    return cipher


#-------------- Decrypting Functions -----------------------------------  


def shift_decrypt(message):
    """ decrypts a cipher thats beeb shifted by 13 ASCII numbers.


        args: A cipher thats been shifted by 13 numbers.


        returns: The decrypted text created by shifting the cipher by
        13 numbers.


    """
    
    text = ""
    alpha = generate_alpha()
    for ch in message:
        num = ord(ch)
        if ch not in alpha:
            text += ch
        elif num - 13 < 31:
           text += chr(127 - (32 - (num - 13)))
        else:
            text += chr(num - 13)


    return text




def rail_decrypt(cipher, n):
    """ Decrypts any transposed cipher, with 'n' amount of rails.


        args:
            cipher: the string that needs to be decrypted.
            n: the length of the password, indicating the amount of rails
            present.


        returns: Text created by dividing the cipher by the # of rails (n), and
        then concatenating the corresponding rail indexes together.
        Each index at rail index 0 will be concatenated using an accumulator,
        then index 1, index 2, etc. until everything has been concatenated.


    """


    #Part 1: Rail seperation
    
    rails = []
    for i in range(n):
        rail_length = len(cipher) // (n - i)
        if len(cipher) % (n - i) != 0:
            rail_length += 1
            rails.append(cipher[:rail_length])
            cipher = cipher[rail_length:]
        else:
            rails.append(cipher[:rail_length])
            cipher = cipher[rail_length:]


    #Part 2: Reconstruction of original text
            
    text = ""
    counter = 0
    for i in range(len(rails[0])):
        for j in range(n):
            if len(rails[j]) != len(rails[0]):
                rails[j] += " "
                counter += 1
            text += rails[j][i]
    the_list = list(text)
    if " " in the_list:
        del the_list[(-1 * counter):]
    text = make_list_string(the_list)
    
    return text


#-------------- Misc --------------------------------------------------


def make_list_string(alist):
    """ Creates a string out of a list.


        args:
            alist: The list whose contents will be converted into a string


        returns: a string with the list's contents.


    """
    
    string = ""
    for x in alist:
        string = string + x
    return string
    
def remove_duplicates(string):
    """ removes any duplicate characters in a string.


        args:
            string: A string from which the duplicate characters will be removed.


        returns: A string with no duplicate characters.


    """


    result = ""
    for ch in string:
        if ch not in result:
            result += ch
    return result


def remove_matches(alpha, minipass):
    """ Removes the characters in the password from the printable alphabet.


        args:
            alpha: All of the ASCII printable characters, 32 - 126
            minipass: The password after it is called in "remove_duplicates()".


        returns: an alphabet that contains no characters from the minipass.


    """
    
    result = ""
    for ch in alpha:
        if ch not in minipass:
            result += ch
    return result


#generates the entire alphabet of printable characters (32 - 126)
def generate_alpha():
    alpha = ""
    for x in range(32, 127):
        alpha += chr(x)
    return alpha


def create_key(alpha, minipass):
    """ Creates a key which is used for substitution encrypting/decrypting.


        This key is created from the password. The keys string indexes are
        matched with the alphabets string indexes, and from there the file
        is either encrypted or decrypted.


        args:
            alpha: ASCII code characters 32 - 126
            minipass: The password without any duplicated characters.


        returns: A key of 94 characters. The minipass is at the beginning of
        the key, followed by the alphabet starting at the character after the
        last character in the password. Then, the preceding alphabet is added
        on to the end.


    """
    
    last_ch = minipass[-1]
    i = alpha.find(last_ch)
    alpha1 = remove_matches(alpha[i + 1:], minipass)
    alpha2 = remove_matches(alpha[:i + 1], minipass)
    return minipass + alpha1 + alpha2


def create_string_from_file(filename):
    """ creates a string from the contents of a file.


        args:
            The file whos contents will be converted into a string.


        returns: A string containing the contents of the file.


    """
    
    open_file = (filename)
    text = ""
    for line in open_file:
        text += line


    return text


#-------------- Main --------------------------------------------------
        
def main():
    """ This function either encrypts or decrypts a function based off of
        user input. It then writes the encrypted/decrypted contents to a file.
        Dont forget your password, because that is the only way to get your
        encrypted file decrypted correctly!


    """
    
    alpha = generate_alpha()
    method = input("Operation (encrypt, decrypt, exit): ")


    if method == "exit":
        return "Goodbye!"


    if method != "encrypt" and method != "decrypt"  and method != "exit":
        return "Invalid Choice! Please select one of the three options"
    
    filename = open(input("Choose a file: "))
    out_file = input("Please choose an output file: ")
    password = input("Password: ")
    n = len(password)


    if method == "encrypt":
        #creates a string from lines in the file
        contents = create_string_from_file(filename)


        #creates a key based off of the password
        key = create_key(generate_alpha(), remove_duplicates(password))
        


        #sub encrypts the contents of the file
        cipher1 = sub_encrypt(contents, generate_alpha(), key)
        
        #transposes cipher1 using n rails (n = length of the password)
        n = len(password)
        cipher2 = transpose_encrypt(cipher1, n)
    
        #shift encrypts cipher2 by 13 shifts
        cipher3 = shift_encrypt(cipher2)


        #writes the encrypted information to a new file
        outfile = open(out_file, "w")
        for line in cipher3:
            outfile.write(line)


        return cipher3
        
    elif method == "decrypt":
        #creates a string from lines in the file
        contents = create_string_from_file(filename)


        #creates a key based off of the password
        key = create_key(generate_alpha(), remove_duplicates(password))


        #uses shifting to decrypt the initial contents of the file
        text1 = shift_decrypt(contents)


        #then, a rail decrypt is used to decrypt text1
        text2 = rail_decrypt(text1, n)


        #finally, decrypts text2 using the same sub_encrypt function
        text3 = sub_encrypt(text2, key, alpha)


        #writes the decrypted information into a new file
        outfile = open(out_file, "w")
        for line in text3:
            outfile.write(line)


        return text3


    filename.close()
    outfile.close()