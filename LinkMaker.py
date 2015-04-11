import urllib2
import os

def ParseAbcInfo(line):
    return line.split(':')[1].strip()

def WriteMarkov(firstLink, secondLink, tuneType, tuneKey):

    if firstLink.strip() == '' or secondLink.strip() == '':
        print("Issue at {}|{}".format(firstLink, secondLink))
    folder = 'data/{}/{}'.format(tuneType, tuneKey)
    if not os.path.exists(folder):
        os.makedirs(folder)
    fileName = "{}/MarkovLinks.txt".format(folder)
    markovFile = open(fileName, 'a')
    markovFile.write('{} | {}\n'.format(firstLink, secondLink))
    markovFile.close()

def ParseAbcFile(abcFileName, tuneType, tuneKey):
    currentPhrase = "start"
    tuneName = ''
    abcFile = open(abcFileName, 'r')
    for line in abcFile:
        if 'Z:' in line or 'S:' in line or 'M:' in line or 'L:' in line:
            continue
        if 'X:' in line:
            tuneNumber = ParseAbcInfo(line)
            if tuneNumber != '1':
                print("New tune {}".format(tuneNumber))
                WriteMarkov(currentPhrase, 'end', tuneType, tuneKey)
                currentPhrase = "start"

        elif 'T:' in line:
            tuneName = ParseAbcInfo(line)
        elif 'R:' in line:
            if tuneType != ParseAbcInfo(line):
                print("Tune type mismatch!")
        elif 'K:' in line:
            if tuneKey != ParseAbcInfo(line):
                print("Tune key mismatch!")
        elif line.strip() == '':
            continue
        elif '|' in line:
            # This is a part of the tune
            editedLine = line.strip()
            editedLine = line.replace(':','')
            for phrase in editedLine.split('|'):
                editedPhrase = phrase.strip()
                if(editedPhrase == ''):
                    continue
                WriteMarkov(currentPhrase, editedPhrase, tuneType, tuneKey)
                currentPhrase = editedPhrase                
        else:
            continue
    abcFile.close()
    WriteMarkov(currentPhrase, 'end', tuneType, tuneKey)
    return True

tuneType = 'reel'
tuneKey = 'Dmaj'
folder = 'data/{}/{}'.format(tuneType, tuneKey)

os.remove("{}/MarkovLinks.txt".format(folder))
for abcFileName in os.listdir(folder):
    if 'abc' in abcFileName:
        fullAbcFileName = "{}/{}".format(folder, abcFileName)
        print("Processing {}".format(fullAbcFileName))
        ParseAbcFile(fullAbcFileName, tuneType, tuneKey) 
