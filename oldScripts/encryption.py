import pyAesCrypt
import sys
import os

# buffersize
bufferSize = 64 * 1024
# encrypts the file with password and file name
def encrypt(password, fileName):
    pyAesCrypt.encryptFile(fileName, fileName+".aes", password, bufferSize)
    if os.path.exists(fileName):
        os.remove(fileName)
# decrypt file with password and file name
def decrypt(password, fileName):
    pyAesCrypt.decryptFile(fileName + ".aes", fileName, password, bufferSize)
    if os.path.exists(fileName+".aes"):
        os.remove(fileName+".aes")

def main():
    done = False
    # runs until the user quits
    while(not done):
        print("Do you want to encrypt, decrypt, or quit? (E/D/Q)")
        answer = input().lower().strip()
        #if user wants to encrypt
        if(answer == "e"):
            print("Enter name of file to encrypt: ")
            fileName = input().strip()
            print("Enter password: ")
            password = input().strip()
            try:
                encrypt(password, fileName)
            except IOError:
                print("ERROR file does not exist")
        # if user wants to decrypt
        elif (answer == "d"):
            print("Enter name of file to decrypt: ")
            fileName = input().strip()
            print("Enter password: ")
            password = input().strip()
            try:
                decrypt(password, fileName)
            except IOError:
                print("ERROR file is not encrypted")
            except ValueError:
                print("ERROR password is incorrect")
        # if user wants to quit
        elif (answer == "q"):
            done = True
            break
        else:
            print("Sorry that is not an option")

if __name__ == '__main__':
    main()