import os
import hashlib
import time
import random
from tqdm import tqdm

#set start time of the script
os.system('cls' if os.name =='nt' else 'clear')         #clear terminal window
output = "hashes.txt"#input("Choose HashFileName :")    #define output-file
input  = "hashes.txt"#input("Input File with Hashes : ")#define input-file for decrypt loop
solved = "solvedhashes.txt"#input("Where to deposit the solved Hashes")#define output-file
mathbound = 10000                                      #max bound for password and salt creation 0 -> mathbound
how_many_passwords = 100                                 #define how many passwords should be generated
randomsalt = random.randint(0,mathbound)                #create random salt variable to import into salt creation
pwcomplexity = mathbound*mathbound                      #necessary for tqdm-progressbar
progress = tqdm(int(pwcomplexity),total = pwcomplexity) #create tqdm-progressbar that lists all possible combinations

def encrypt(output):                      #function to encrypt salted passwords with sha256
    #check if output file already exists  
    #output = "hashes.txt"                #choose output file
    if os.path.isfile(output) != True:    #probes if the output file exists
     open(output,'x').close()             #if it doesn't exist create it and close it
    else :                                #clear existing output file
     open(output,"w").close()             #open output file in write mode to clear it and close it
    how_many = how_many_passwords         #int(input("How many Passwords"))
    while how_many != 0 :                 #hash generation loop
     #set password and salt
     randomint = random.randint(0,mathbound)#generate random password
     password = str(randomint)            #input("Gimme PassWord pls : ")
     salt = str(randomsalt)               #salt the password to make it harder to crack
     pws = password+salt                  #combine password and salt to encode it
     encodedpws = pws.encode()            #encode the string to make it usable in the hash function
     #create hash
     hash= hashlib.sha256(encodedpws)     #convert encoded string into a sha256 hash
     #write hash  to output file
     fileappend = open(output,'a')        #open outputfile in append mode
     readablehash = hash.hexdigest()      #convert the hash from object to string
     fileappend.write(readablehash)       #write hash into outputfile
     fileappend.write("\n")               #add \n to set the file pointer to the next line
     fileappend.close()                   #close append for optional testing cycle
     how_many = how_many -1               #counter
    return output 
def decrypt(inputfile,solved) :           #function to decrypt hashed and salted sha256 passwords
    start_time = time.time()
    salt_found = 0
    #inputfile = "hashes.txt"
    if os.path.isfile(inputfile) == False:#checks if the inputfile exists
        print("file does not exist") 
        return                            #prints error if the file does not exist
    if os.path.isfile(inputfile) == True: #if the input file exists open it in read mode
     readfile = open(inputfile,'r')       #open file in read mode
    #create solvedfile
    lines = readfile.readlines()          #set lines as all lines in the readfile
    if os.path.isfile(solved) != True:    #if the solvedfile does not exist create it
        open(solved,'x').close()          #create solvedfile
    else : #clear output file 
     open(solved,"w").close()             #clear solvedfile if it alread exists
    #crack each line in the file
    for line in lines :                   # for each line in the input file (boundary-loop)
      cracked = False                     # set cracked as false until changed in the inner while loop
      while cracked == False :            # while hash in line is not cracked (outer-loop)
         counter  = 0
         counter2 = 0
         while counter2+1 < mathbound :        # while counter in range of usable characters (inner-loop)
             progress.update()                 # for each tested password+hash update progressbar
             password = str(counter)           # set password to counter
             if salt_found == 0:               # if salt has not yet been found
                 salt = str(counter2)          # set salt to counter2
             else:                             # when salt has been found 
                salt = str(salt_found)         # set salt as found_salt
             passwordsalt = password+salt      # combine password and salt
             encoded = passwordsalt.encode()   # encode password to match hashlib requirements
             hash = hashlib.sha256(encoded)    # hash passwort to make it comparable
             comparablehash = hash.hexdigest() # outout hash as str
             counter = counter +1              # make counter higher to make the counter usable
             if comparablehash+"\n" == line :  # when password+salt equals saved hash print to solve file 
                 solvedfile = open(solved,'a') # open file to deposit solved hashes 
                 solvedfile.write("password :"+password+" salt :"+salt+" = "+comparablehash+"\n") #pretty password print
                 solvedfile.close()
                 cracked = True                # set cracked = true to break outer while
                 if salt_found == 0:           # update salt_found when salt is found
                     salt_found = counter2     # set salt_found to counter2
                 counter2 = mathbound          # set counter2 to max to break inner while
             if counter+1 == mathbound:        # when counter / password combinations run through 
                 counter = 0                   # set counter back to the beginning of the combinations
                 counter2=counter2+1           # set salt combination counter higher       
    print(" Decryption completed: ",time.time()-start_time) # statement to obtain time the script took to finish

encrypt(output)                                # call encrypt-def
decrypt(input,solved)                          # call decrypt-def