#!/usr/bin/python
import mailbox
import subprocess
import argparse

#####################################################################
# Prompts user to choose which search to do
#   return: number of input choice (between x-x)
def getChoice():
    print("")
    print("Please choose an option from the list below:")
    print("  1) Run KODA on emails which contain a specific keyword")
    print("  2) Run KODA on emails written from a certain person")
    print("  3) Run KODA on emails written to a certain person")
    print("  4) Run KODA on emails sent between two people")
    print("  5) Run KODA on emails sent on a specific day")
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
        
    print("___________________________________________________________")
    return choice


#####################################################################
# Searches through mbox for emails containing a certain keword
def keywordSearch(path, outfile):
    count = 0
    print("")
    searchTerm = raw_input("  Please enter a search term:")
    for message in mailbox.mbox(path):
        print (message['subject'])
        if searchTerm in str(message):
            count = count + 1
            print (message)
            outfile.write(str(message))


#####################################################################
# Searches through mbox for emails sent by a certain person
def senderSearch(path, outfile):
    count = 0
    print("")
    searchTerm = raw_input("  Please enter name of sender:  ")
    print("  Searching for emails from " + searchTerm + "...")
    for email in mailbox.mbox(path):
        if searchTerm in str(email['From']):
            count = count + 1
            body = getBodyFromEmail(email)
            outfile.write(str(body))
            print(body) 
            print("___________________________________________________________")
            print("")

    print("There were " + str(count) + " emails sent by " + searchTerm + ".")


#####################################################################
# Searches through mbox for emails recieved by a certain person
def recipiantSearch(path, outfile):
    count = 0
    print("")
    searchTerm = raw_input("  Please enter name of recipient:  ")
    print("  Searching for emails to " + searchTerm + "...")
    for email in mailbox.mbox(path):
        if searchTerm in str(email['To']):
            count = count + 1
            body = getBodyFromEmail(email)
            outfile.write(str(body))
            print(body) 
            print("___________________________________________________________")
            print("")

    print("There were " + str(count) + " emails recieved by " + searchTerm + ".")


#####################################################################
# Searches through mbox for emails between two people
def conversationSearch(path, outfile):
    count = 0
    print("")
    searchTerm1 = raw_input("  Please enter name of person 1:  ")
    searchTerm2 = raw_input("  Please enter name of person 2:  ")
    print(" Searching for emails between " + searchTerm + " and " + searchTerm2 + "...")
    for email in mailbox.mbox(path):
        if searchTerm1 in str(email['From']) and searchTerm2 in str(email['To']):
            count = count + 1
            body = getBodyFromEmail(email)
            outfile.write(str(body))
            print(body) 
            print("___________________________________________________________")
            print("")
        elif searchTerm1 in str(email['To']) and searchTerm2 in str(email['From']):
            count = count + 1
            body = getBodyFromEmail(email)
            outfile.write(str(body))
            print(body) 
            print("___________________________________________________________")
            print("")

#####################################################################
# Searches through mbox for emails during a certain month
def dateSearch(path, outfile):
    print("")
    searchTerm = raw_input("  Please enter date in form of 'Mon, 7 Jan 2002':  ")
    print("  Searching for emails sent on " + searchTerm + "...")
    for email in mailbox.mbox(path):
        if searchTerm in str(email['Date']):
            body = getBodyFromEmail(email)
            outfile.write(str(body))
            print(body) 
            print("___________________________________________________________")
            print("")


#####################################################################
# Tests loop through files for Maildir  (otherwise same format for getting info from emails)
def mailDirTest(path, outfile):
    for dirname, subdirs, files in os.walk(path):
        print dirname
        print '\tDirectories:', subdirs
        for name in files:
            fullname = os.path.join(dirname, name)
            print
            print '***', fullname
            #print open(fullname).read()
            print '*' * 20


#####################################################################
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


#####################################################################
# Gets body of an email (edited this method from a stack overflow example)
#   return: body of email that is in mbox form
def getBodyFromEmail(msg):
    body = None
    #Walk through the parts of the email to find the text body.    
    if msg.is_multipart():    
        for part in msg.walk():

            # If part is multipart, walk through the subparts.            
            if part.is_multipart(): 

                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True) 
                        #charset = subpart.get_charset()

            # Part isn't multipart so get the email body
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                #charset = part.get_charset()

    # If this isn't a multi-part message then get the payload (i.e the message body)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 

   # No checking done to match the charset with the correct part. 
    for charset in getCharSets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            print("Unicode Decode Error...")
        except AttributeError:
             print("Attribute Error...")
    return body


#####################################################################
# Gets the set of characters in the message (in case wierd ones)
#   return: list of characters in message
def getCharSets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

#####################################################################
# Runs parsedoc.exe on the current temp file, in theory.   
# Still needs to be tested on a working parsedoc.exe, and
# will need something built to put the output into a text file.
def runKODAOnCurrentFile(count):
    print('Running KODA on tempKODAfile' + str(count) + '.txt')
    kodaOutput = subprocess.check_output(['./parsedoc', 'tempKODAfile' + str(count) + '.txt', '5'])
    writeFile = open('KODAoutputfile'+str(count)+'.txt', 'w')
    writeFile.write(str(kodaOutput))
    writeFile.close()



#####################################################################
# Main method that runs everything! :D
def main():

    parser = argparse.ArgumentParser(description="File input")
    parser.add_argument('-i', '--input', help='take the filepath of an mbox file as input.')
    args = parser.parse_args()
    if(args.input):
        mboxfile = args.input
    else:
        mboxfile = "F:\Documents and Settings\skylar.downes\Application Data\Thunderbird\Profiles\lwac8qob.default\Mail\Local Folders\Outlook Express Import.sbd\Inbox"  #"C:\Python27\Enron\Inbox"
    
    print("Welcome to your friendly neighborhood mbox-mail-file-to-KODA-output program!")

    count = 1
    while True:
        writeFile = open('tempKODAfile'+str(count)+'.txt', 'w')
        userChoice = getChoice()
        if (userChoice == 1):
            keywordSearch(mboxfile, writeFile)
        elif (userChoice == 2):
            senderSearch(mboxfile, writeFile)
        elif (userChoice == 3):
            recipiantSearch(mboxfile, writeFile)
        elif (userChoice == 4):
            conversationSearch(mboxfile, writeFile)
        elif (userChoice == 5):
            dateSearch(mboxfile, writeFile)
        writeFile.close()
        runKODAOnCurrentFile(count)
        num = continueLoop()
        if(num == 1):
            print("")
            print("Starting another search...")
            print("_________________________________________________________")
            count = count + 1
            continue
        else:
            print("")
            print("So long, and thanks for all the fish!")
            break

#####################################################################
# run the program
main()

###############################
# For getting the 'subject' of an email
#   
def getSubject(email):
    subject = email['subject']


###############################
# For getting the date of an email
#   date = email['date']
def getMailDate(email):
    return str(email['Date'])

###############################
# To loop through files in a directory
#    for filename in os.listdir (folder):    
#    (where 'folder' is the path to the folder you want to loop through)