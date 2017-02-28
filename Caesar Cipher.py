'''
Jocelyn Ao
jao1@binghamton.edu
Lab Section B57
Jia Yang
Assignment 10
'''

'''
This program, given a file, will decrypt or encrypt the file based on
the rotation key that the person wants. The encoded/decoded file will
then be written into a new file

Output to file:
In the new file, the encoded or decoded file is written in there.

Tasks allocated to functions:
convertRotationKey()
keepInBounds()
processMessage()
makeName()
writeToFile()
'''

# Imports --------------------------------------------------------
import string
import os.path

#Constants -------------------------------------------------------

# Mapping of valid operations to rotationKey factor
OPERATIONS = {'e':[1,"Encrypted"], 'd':[-1,"Decrypted"]}

# Min and limit ordinals of printable ASCII
PRINTABLE_ASCII_MIN = 32
PRINTABLE_ASCII_LIMIT = 127
ACCEPTABLE_LARGE_NUMBER = 126

# Allowable rotationKey prefixes
KEY_PREFIX = "-"

# Required file extension
FILE_EXT = ".txt"

# File processing modes
READ_MODE = 'r'
WRITE_MODE = 'w'

# Functions ------------------------------------------------------------------

# Check that requested operation is valid
# param opStr (str) - operation requested
# invoke len()
# invoke str.lower()
# return  True when valid, False otherwise (bool)
def operationValidated(opStr):
    return opStr.lower() in OPERATIONS and len(opStr) == 1
##print(operationValidated('e'))
##print(operationValidated('f'))

# Check that rotation key is of form <digits> or -<digits>
# param rotationKeyStr (str)
# invoke str.isdigit() 
# returns:  True when valid, False otherwise (bool)
def rotationKeyValidated(rotationKeyStr):
    if rotationKeyStr[0] == KEY_PREFIX:
        rotationKeyStr = rotationKeyStr[1:]
    return rotationKeyStr.isdigit()
##print(rotationKeyValidated("4"))
##print(rotationKeyValidated("f"))

# Convert rotation key to value usable for requested operation
# param  op (str) - operation requested 
# param  rotationKeyStr (str)
# invoke int()
# return encryption or decryption rotation key (int)
def convertRotationKey(opStr, rotationKey):
    return (OPERATIONS.get(opStr)[0] * rotationKey)
##print(convertRotationKey('e',24))
##print(convertRotationKey('d', -8))

# Perform string modulus operation to prevent processed character 
# from going out of bounds
# param ordinal (int)
# returns adjusted ordinal of new character (int)
def keepInBounds(ordinal):
    newOrdinalTwo = ordinal
    if newOrdinalTwo != ACCEPTABLE_LARGE_NUMBER or \
       newOrdinalTwo != PRINTABLE_ASCII_MIN:
        while not(newOrdinalTwo < PRINTABLE_ASCII_LIMIT and \
                  newOrdinalTwo > PRINTABLE_ASCII_MIN):
            if newOrdinalTwo == ACCEPTABLE_LARGE_NUMBER or \
               newOrdinalTwo == PRINTABLE_ASCII_MIN:
                return newOrdinalTwo
            elif newOrdinalTwo >= PRINTABLE_ASCII_LIMIT:
                newOrdinalTwo = newOrdinalTwo - \
                                (PRINTABLE_ASCII_LIMIT - PRINTABLE_ASCII_MIN)
            else:
                newOrdinalTwo = newOrdinalTwo + \
                               (PRINTABLE_ASCII_LIMIT - PRINTABLE_ASCII_MIN)
    return newOrdinalTwo
##print(keepInBounds(89))
##print(keepInBounds(-432))

# Encrypt or decrypt message using rotationKey
# param message (str)
# param rotationKey (int)
# invoke keepInBounds()    
# return processedMessage (str)  
def processMessage(message, rotationKey):
    messageOutput = ""
    message.split()
    for ch in message:
        newOrdinal = ord(ch) + rotationKey
        boundedOrdinal = keepInBounds(newOrdinal)
        messageOutput = messageOutput + chr(boundedOrdinal)
    return (messageOutput)
##print(processMessage("fjdskl", 45))
##print(processMessage("jfds", -3))

# Checks that file exists and that extension is .txt
# param name (str) - file name
# invoke isFile() from module os.path and endswith()
# return True when valid, False otherwise (bool)
def fileNameValidated(name):
  return os.path.isfile(name) and name.endswith(FILE_EXT)
##print(fileNameValidated("MidnightCaptainEncrypted127.txt"))
##print(fileNameValidated("CaptainMidnight.txt"))

# Generates output file name from input file name, 
# operation requested and rotation key
# param fileName (str) - input file name
# param operation (str)
# param rotationKey (int) - converted key
# invoke str.split(), str.replace() and str.join()
# return output file name (str)
def makeName(fileName, operation, rotationKey):
  nameList = fileName.split(".")
  nameList[0] = nameList[0].replace(OPERATIONS['e'][1], "")
  nameList[0] = nameList[0].replace(OPERATIONS['d'][1], "")
  nameList[0] += (OPERATIONS[operation][1] + str(rotationKey))
  return ".".join(nameList)
##print(makeName("CaptainMidnight.txt", "e", 4))
##print(makeName("CaptainMidnightEncrypted5.txt", "d", 40))

# Given a list of characters, writes this list to a new file given\
#  the file name
# param file (_io.TextIOWrapper)
# param anylist (list)
# invoke write()
def writeToFile(file, anylist):
    for line in anylist:
   # for ch in line:
        file.write(line + "\n")
    #file.write('\n')
##anylist = ['x7FJ7?DU#?:D?=>JU7D:UJ>;U)']
##file = "hello.txt"
##writeToFile(file, anylist)

# Main ---------------------------------------------------------------

# Gets a file, operation requested, and the rotation key. It then either
#  decrypts or encrypts and afterward, writes the new set of lines into
#  a new file
def main():
    # Describess program
    print("This program encrypts or decrypts messagaes" + \
          "using a Caesar cipher")
    # Priming read and repeat
    secretFile = input("Please enter the file or press <Enter> to quit")
    while secretFile:
        # Get remaining inputs, validate and convert as necessary
        while not fileNameValidated(secretFile):
            print("Invalid input, try again")
            secretFile = input("Please enter the file or press <Enter> to quit")
        operation = input("Enter 'D/d' or 'E/e' for either decryption or" + \
                     "encryption")
        while not operationValidated(operation):
            print("Invalid input, try again")
            operation = input("Enter 'D/d' or 'E/e' for either decryption" + \
                         "or encryption")
        rotationKeyStr = input("Enter the rotation key")
        while not rotationKeyValidated(rotationKeyStr):
            print("Invalid input, try again")
            rotationKeyStr = input("Enter the rotation key")
        rotationKey = convertRotationKey(operation, int(rotationKeyStr))
        # Creates the new file name where the message will be written to
        newFile = (makeName(secretFile, operation, rotationKey))
        listLines = []
        # Tries to open the new file
        try:
            readFile = open(secretFile, READ_MODE)
            try:
                # Tries to read the file and then splits it so that the\
                #  newline characters will not be included
                readList = readFile.read()
                readList = readList.split('\n')
                for aline in readList:
                    # Encrypts or decrypts contents of file
                    newLine = processMessage(aline, rotationKey)
                    # Adds the new encrypted/decrypted lines into a list
                    listLines.append(newLine)
                # Tries to open the new file to be written in
                try:
                    writeFile = open(newFile, WRITE_MODE)
                    try:
                        # Tries to send the new file name and the list of \
                        #  encoded or decoded lines so that the lines can\
                        #  be written to the new file
                        writeToFile(writeFile, listLines)
                    except IOError as err: # inner exception handler \
                        #for outfile processing
                        print("\nProblem writing data: \n" + str(err))
                    except ValueError as err:  # inner exception handler\
                        #for outfile processing
                        print("\nProblem writing data, wrong format\
or corrupted?  \n" + str(err) + '\n')
                    except Exception as err: # inner exception handler\
                        #for outfile processing
                        print("\nData cannot be written to file: \n" +\
                              str(err) + '\n')
                    finally:# will close file whether or not exception \
                        #has been raised
                        writeFile.close()
                except IOError as err: # "outer" exception handler for\
                    #outfile open
                    print("\nExecption raised during open of output file,\
no write performed: \n" + str(err) + '\n')
                except Exception as err: # outer exception handler for \
                    #outfile processing
                    print("\nData cannot be read:  \n" + str(err) + '\n')
            except IOError as err: # inner exception handler for\
                #infile processing
                print("\nProblem reading data: \n" + str(err))
            except ValueError as err: # inner exception handler for \
                #infile processing
                print("\nProblem processing data, wrong format or \
corrupted? \n" + str(err) + '\n')
            except Exception as err: #inner exception handler \
                #for infile processing
                print("\nData cannot be read:  \n" + str(err) + '\n')        
            finally:#will close file whether or not exception has been raised
                readFile.close()
        except FileNotFoundError as err:  # outer exception\
            #handler for infile open
            print("\nFile not found:  deleted or in wrong folder?\
\n" + str(err) + '\n')
        except IOError as err: # outer exception handler for infile open
            print("\nException raised during open of input file, \
try a different file: \n" + str(err) + '\n')
        except Exception as err: # outer exception handler for infile open
            print("\nData cannot be read:  \n" + str(err) + '\n')
        secretFile = input("Please enter the file or press" +\
                              "<Enter> to quit")

main()
