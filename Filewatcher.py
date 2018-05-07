# -------------------------------------------------------#
#                     FILEWATCHER                        #
#               Author: Deepjyoti Barman                 #
#                  Github: deepjyoti30                   #                       
#--------------------------------------------------------#


# It will compare two text files and check the differences in the files.
# Two filenames would be taken as input.
# One will be considered old and the other new
# Lets test my filewatcher!

from __future__ import print_function
from colorama import init, Fore, Style
import os, sys, shutil

init()

removedLines = []
addedLines = []

old_file = ''
new_file = ''

def allot_names(param, new_one = '', old_one = ''):
    # The name allotment will be controlled by the param passed.
    if param == 1:
        old_file = old_one  #input("Enter the old file destination -: ")
        new_file = new_one  #input("Enter the new file destination -: ")
    elif param == 2:
        old_file = sys.argv[1]
        new_file = sys.argv[2]
    else:
        pass
    check_if_available(old_file, new_file)
    main(old_file, new_file)

# It will check if the files are available or not.

def check_if_available(old_file, new_file):
    if not os.path.isfile(old_file) or not os.path.isfile(new_file):
        return False
    else:
        return True

# ---------------------check saved-----------------------------
# Execute the filewatcher on the saved files in the folder.
# First search for the Filewathcer folder in the current folder.
# Then get the name of the file in it and compare with the file of the same name in the current folder.

def check_saved():
    if not os.path.isdir(os.getcwd() + '\Filewatcher'):
        print(' Filewatcher folder not found!\a : Process stopped!')
        return -1
    else:
        for files in os.listdir('Filewatcher'):
            old_ones_name = 'Filewatcher\\' + files
            new_ones_name = files
            allot_names(1, new_ones_name, old_ones_name)


# --------------------commit ---------------------------------
# This will merge the changes in the new filw to the old one.
# That is copy the new file to the directory Filewatcher.

def commit():
    # Check if Filewatcher folder present
    if not os.path.isdir('Filewatcher'):
        print('Please follow the guidelines')
    else:
        for files in os.listdir('Filewatcher'):
            name = files
            os.remove('Filewatcher\\' + name)
            for file_name in os.listdir(os.getcwd()):
                if file_name == name:
                    shutil.copyfile(name, 'Filewatcher\\' + name)
                    print(Fore.LIGHTCYAN_EX + ' -- Done!' + Style.RESET_ALL)
                    return True
            print(name + ' was not found!\a ERROR!')


#--------------------------setup----------------------------
# Running the setup command will setup the filewatcher in the folder where it is run.
# Usage: python filewatcher.py [filename]
# filename should be a source file.

def setup(filename):
    # Make the folder
    try:
        for files in os.listdir(os.getcwd()):
            if files == 'Filewatcher' and os.path.isdir('Filewatcher'):
                print('Folder already exists! Delete it first and run the command again! \a')
                return False
        os.mkdir('Filewatcher')
    except:
        print('\aFailed! Check if the folder already exists.')
    # Copy the file their
    shutil.copyfile(filename, 'Filewatcher/' + filename)
    print(' -- Done! ')

# ------------------------Usage--------------------------------
def show_Usage():
    print(Fore.LIGHTBLUE_EX, end = '')
    print(' USAGE: python filewatcher.py [option(s)]')
    print(' Available options : ')
    print(Fore.GREEN + ' --> setup [sourcefile]' + Style.RESET_ALL)
    print(' It will setup the sourcefile as the base to compare to changes made to the new file.')
    print(" A folder will be created by the name 'Filewatcher'. DON'T DELETE IT!")
    print(Fore.GREEN + ' --> -c ' + Style.RESET_ALL)
    print(' It will commit the changes made to the sourcefile backed up in the folder Filewatcher.')
    print(Fore.GREEN + ' --> [old Filename] [New filename]' + Style.RESET_ALL)
    print(' This will compare the old file to the new file and show what changes are made to the new one.')
    print(Fore.GREEN + ' --> -h ' + Style.RESET_ALL)
    print(' Show these menu')
    print(Fore.RED + ' Calling without any arguements will make it compare the sourcefile saved in setup and show the changes made to it' + Style.RESET_ALL)

def show_error():
    print(Fore.RED, end = '')
    print('\aPlease pass proper arguements!')
    print(' For Help: python filewatcher.py -h ')
    print(Style.RESET_ALL, end = '')

#--------------------------print--------------------------------------
# The removed lines will be shown with a minus (-) sign in the beginning
# The added lines will be shown with a plus(+) sign in the beginning

def print_removed():
    for line in removedLines:
        print(Fore.RED + ' - ' + line + Style.RESET_ALL)

def print_added():
    for line in addedLines:
        print(Fore.GREEN + ' + ' + line + Style.RESET_ALL)

#------------------main---------------------------------------

def isAvailable(line, fileToCheck):
    # Check if line is available in file
    read_FILE = open(fileToCheck, 'r')
    while True:
        lineRead = read_FILE.readline()
        if not lineRead:
            return False
        if lineRead == line:
            return True

def create_removedLines(old_file, new_file):
    # This will add all the lines that are present in old but not in new.
    count_line = 0
    old = open(old_file, 'r')
    while True:
        line = old.readline()
        if not line:
            break
        count_line += 1
        if not isAvailable(line, new_file):
            rem_line = str(count_line) + ' ' + line
            removedLines.append(rem_line)

def create_addedLines(old_file, new_file):
    # This will add all the lines that are present in new file but not in the old.
    count_line = 0
    new = open(new_file, 'r')
    while True:
        line = new.readline()
        if not line:
            break
        count_line += 1
        if not isAvailable(line, old_file):
            add_line = str(count_line) + ' ' + line
            addedLines.append(add_line)

#------------------------------------------------------

#--------------------------extract command------------------------
# The passed arguement will be extracted and executed.

def execute():
    if len(sys.argv) == 3 and sys.argv[1] == 'setup':
        setup(sys.argv[2])
    elif len(sys.argv) == 1:
        # exec the filewatcher on the file saved in the folder
        check_saved()
    elif len(sys.argv) == 2 and sys.argv[1] == '-c':
        # replace the file in the folder with the changed one
        commit()
    elif len(sys.argv) == 3:
        # simply compare the passed files.
        allot_names(2)
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        show_Usage()
    else :
        show_error()


def main(old_file, new_file):
    create_removedLines(old_file, new_file)
    create_addedLines(old_file, new_file)
    if len(removedLines) == 0 and len(addedLines) == 0:
        print(Fore.BLUE + 'No Changes!\a' + Style.RESET_ALL)
    else: 
        print(Fore.LIGHTCYAN_EX + ' -- Line numbers are according to the file -- || Press any key!' + Style.RESET_ALL)
        input()
        print_removed()
        print()
        print_added()

execute()
    






        