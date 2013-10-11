#!/usr/bin/python
import mailbox
import subprocess

###############################
# Prompts user to choose which search to do
#   return: number of input choice (between x-x)
def getChoice():
    print("")
    print("Please choose an option from the list below:")
    print("  1) Run KODA on emails which contain a specific keyword")
    print("  2) Run KODA on emails written by a certain person")
    print("  3) Run KODA on emails written to a certain person")
    print("  4) Run KODA on emails sent between two people")
    print("  5) Run KODA on emails during a specific month")
    print("")

    choice = -1
    
    while True:
        try:
            choice = int(raw_input("Enter a number between 1 and 5: "))
        except ValueError:
            print("  Invalid Input:")
            print("  Please enter a whole number.")
            print("")
            continue
        if(choice > 5 or choice < 1):
            print("  Invalid Input:")
            print("  Please enter a number between 1 and 5.")
            print("")
            continue
        else:
            break

    return choice


###############################
# Searches through mbox for emails containing a certain keword
def keywordSearch():
    print("")
    searchTerm = input("  Please enter a search term:")
            for message in mailbox.mbox(mboxfile):
                print (message['subject'])
                if searchTerm in str(message):
                    print (message)
                    writeFile.write(str(message))


###############################
# Searches through mbox for emails sent by a certain person
def senderSearch():
    print("")
    searchTerm = input("  Pleae enter name of person who sent the emails:")
            for message in mailbox.mbox(mboxfile):
                print (message['subject'])
                if searchTerm in str(message['From']):
                    print (message)
                    writeFile.write(str(message))
                ###############################
                # For getting the sender(s) of an email (or 'message' in above for loop)
                #   sender = email['from']


###############################
# Searches through mbox for emails recieved by a certain person
def recipiantSearch():
    print("")
    searchTerm = input("  Pleae enter name of person who recieved the emails:")
            for message in mailbox.mbox(mboxfile):
                print (message['subject'])
                if searchTerm in str(message['To']):
                    print (message)
                    writeFile.write(str(message))
                ###############################
                # For getting the recipient(s) of an email
                #   recip = email['to']


###############################
# Searches through mbox for emails between two people
def conversationSearch():
    print("  not built yet")


###############################
# Searches through mbox for emails during a certain month
def dateSearch():
    print("  not built yet")


###############################
# Prompts user to do another search or cease
#   return: 1 if yes, 0 if no, -1 if something broke 
def continueLoop():
    print("")
    print("Do you want to do another search?")
    out = -1
    
    while True:
        try:
            choice = raw_input("(Y/N): ").lower()
            if(choice == "y" or choice == "yes"):
                out = 1
            elif(choice == "n" or choice == "n"):
                out = 0
        except ValueError:
            print("  Invalid Input:")
            print("")
            continue
        else:
            break

    return out

###############################
# Main method that runs everything! :D
def main():
    mboxfile = "C:\Python27\Enron\Inbox"
    print("Welcome to your friendly neighborhood mbox-mail-file-to-KODA-output program!")

    while True:
        writeFile = open('tempKODAfile.txt', 'w')
        userChoice = getChoice()
        if (userChoice == 1):
            keywordSearch()
        elif (userChoice == 2):
            senderSearch()
        elif (userChoice == 3):
            recipiantSearch()
        elif (userChoice == 4):
            conversationSearch()
        elif (userChoice == 5):
            dateSearch

        writeFile.close()
        num = continueLoop()
        if(num == 1):
            print("")
            print("Starting another search...")
            print("_________________________________________________________")
            continue
        else:
            print("")
            print("So long, and thanks for all the fish!")
            break

        

# Need to build something to call tempKODAfile.txt here

#####################################################################
# run the program
main()

###############################
# For getting the 'subject' of an email
#   subject = email['subject']

###############################
# For getting the date of an email
#   date = email['date']

###############################
# To loop through files in a directory
#	for filename in os.listdir (folder):    
#	(where 'folder' is the path to the folder you want to loop through)
