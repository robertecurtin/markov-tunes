import urllib2
import os

def ParseAbcInfo(line):
    return line.split(':')[1].strip()

def WriteMarkov(firstLink, secondLink, tuneType, tuneKey):

    folder = 'data/{}/{}'.format(tuneType, tuneKey)
    if not os.path.exists(folder):
        os.makedirs(folder)
    fileName = "{}/MarkovLinks.txt".format(folder)
    markovFile = open(fileName, 'a')
    markovFile.write('{} | {}\n'.format(firstLink, secondLink))
    markovFile.close()

def MarkCompleted(tuneType, tuneKey):
    tuneCountFile = 'data/{}/{}/NumberOfTunes.txt'.format(tuneType, tuneKey)
    if not os.path.isfile(tuneCountFile):
        counterFile = open(tuneCountFile, 'w')
        counterFile.write('1')
        counterFile.close()
    else:
        counterFile = open(tuneCountFile, 'w+')
        line = counterFile.read()
        if line == '':
            counterFile.write('1')
            counterFile.close()
        else:
            numTunes = int(counterFile.read()) + 1
            counterFile.write(str(numTunes))
            counterFile.close()
    

def ParseAbcFile(abcFile):
    currentPhrase = "start"
    tuneType = ''
    tuneKey = ''
    for line in abcFile:
        if 'X:' in line or 'Z:' in line or 'S:' in line or 'M:' in line or 'L:' in line:
            continue
        elif 'T:' in line:
            tuneName = ParseAbcInfo(line)
        elif 'R:' in line:
            tuneType = ParseAbcInfo(line)
        elif 'K:' in line:
            tuneKey = ParseAbcInfo(line)
        elif line.strip() == '':
            continue
        elif '|' in line:
            # This is a part of the tune
            editedLine = line.rstrip()
            for phrase in editedLine.split('|'):
                if(phrase == ''):
                    continue
                WriteMarkov(currentPhrase, phrase, tuneType, tuneKey)
                currentPhrase = phrase                
        else:
            continue
    WriteMarkov(currentPhrase, 'end', tuneType, tuneKey)
    MarkCompleted(tuneType, tuneKey)
    return True

errors = 0
successes = 0
for i in range(6000,7000):
    fileName = 'https://thesession.org/tunes/{}/abc/1'.format(i)
    try:
        response = urllib2.urlopen(fileName)
        success = ParseAbcFile(response)
        if success:
            print("{} was processed correctly!".format(fileName))
        response.close()
    except:
        print("Error with {}".format(fileName))
        errors += 1
print('{} errors'.format(errors))
    
