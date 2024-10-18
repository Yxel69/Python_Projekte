import os
import hashlib
import time
import random
import string
from tqdm import tqdm

# Set start time of the script
os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal window
output = "hashes.txt"  # define output-file
input = "hashes.txt"  # define input-file for decrypt loop
solved = "solvedhashes.txt"  # define output-file for solved hashes
password_length = 2  # define the length of the password
salt_length = 1  # define the length of the salt
how_many_passwords = 1  # define how many passwords should be generated

# Character set for alphanumeric passwords and salts
characters = string.ascii_letters + string.digits

# Progress bar setup based on total combinations possible
pwcomplexity = len(characters) ** (password_length + salt_length)
progress = tqdm(total=pwcomplexity)  # create tqdm progress bar

def generate_random_string(length):
    """Helper function to generate a random alphanumeric string of a given length."""
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt(output):
    """Function to encrypt alphanumeric passwords with a random salt using sha256."""
    if not os.path.isfile(output):
        open(output, 'x').close()  # if it doesn't exist, create it
    else:
        open(output, "w").close()  # clear the existing file
    
    for _ in range(how_many_passwords):
        # Generate random password and salt
        password = generate_random_string(password_length)
        salt = generate_random_string(salt_length)
        pws = password + salt  # combine password and salt
        encoded_pws = pws.encode()  # encode the string for hashing
        hash_obj = hashlib.sha256(encoded_pws)  # create sha256 hash
        readable_hash = hash_obj.hexdigest()  # get the hexadecimal string of the hash

        # Write hash to output file
        with open(output, 'a') as fileappend:
            fileappend.write(readable_hash + "\n")

    return output

def decrypt(inputfile, solved):
    """Function to decrypt hashed and salted sha256 passwords."""
    start_time = time.time()
    salt_found = None
    
    if not os.path.isfile(inputfile):
        print("file does not exist")
        return

    with open(inputfile, 'r') as readfile:
        lines = readfile.readlines()

    if not os.path.isfile(solved):
        open(solved, 'x').close()  # create the solved file if it doesn't exist
    else:
        open(solved, "w").close()  # clear the file if it already exists

    # Crack each line in the input file
    for line in lines:
        cracked = False
        for password_attempt in range(pwcomplexity):
            # Generate password and salt combinations
            for salt_attempt in range(len(characters) ** salt_length):
                progress.update()  # update progress bar
                
                password = generate_random_string(password_length)
                if salt_found is None:
                    salt = generate_random_string(salt_length)
                else:
                    salt = salt_found

                passwordsalt = password + salt
                encoded = passwordsalt.encode()
                hash_obj = hashlib.sha256(encoded)
                comparable_hash = hash_obj.hexdigest()

                if comparable_hash + "\n" == line:
                    with open(solved, 'a') as solvedfile:
                        solvedfile.write(f"password: {password}, salt: {salt} = {comparable_hash}\n")
                    cracked = True
                    salt_found = salt  # Once a salt is found, save it for future use
                    break

            if cracked:
                break

    print("Decryption completed:", time.time() - start_time)

# Call the encryption and decryption functions
encrypt(output)
decrypt(input, solved)
