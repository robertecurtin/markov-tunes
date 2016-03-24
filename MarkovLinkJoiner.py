from random import uniform

def NormalizePhrases(phrases):
    for key, phrase in phrases.iteritems():
        totalConnections = 0.0
        # Sum up all the connections made
        for linkedPhrase, connections in phrase.iteritems():
            totalConnections += connections
        # Normalize those connections into a percentage
        totalPercentage = 0.0
        for linkedKey, connections in phrase.iteritems():
            totalPercentage += 100.0 * float(connections) / float(totalConnections)
            phrases[key][linkedKey] = totalPercentage

def PrepAbcFile(fileName, tuneType, tuneKey):
	abc = open(fileName, 'w')
	abc.write("X: 1\n")
	abc.write("T: Irish Autotuner's Tune\n")
	abc.write("R: {}\n".format(tuneType))
	abc.write("M: 4/4\n")
	abc.write("L: 1/8\n")
	abc.write("K: {}\n".format(tuneKey))
	abc.close()

def CreateMarkovTune(markovLinksFileName):
    markovLinksFile = open(markovLinksFileName)
    phrases =  {}
    for line in markovLinksFile:
        if('|' not in line):
            continue
        chain = line.split('|')
        firstLink = chain[0].strip()
        secondLink = chain[1].strip()
        if firstLink in phrases:
            if secondLink in phrases[firstLink]:
                phrases[firstLink][secondLink] += 1
            else:
                # Initialize the link with 1
                phrases[firstLink][secondLink] = 1
        else:
            # Create the link with its first connection
            phrases[firstLink] = {secondLink:1}

    NormalizePhrases(phrases)
    newTune = ''
    currentPhrase = 'start'
    outputFileName = 'Markovoutput.abc'
    PrepAbcFile(outputFileName, "jig", "Amaj")
    outputFile = open(outputFileName, 'a')
    while 'end' not in currentPhrase:
        random = uniform(0.0, 100.0)
        if currentPhrase not in phrases:
            print("Ending prematurely with {}".format(currentPhrase))
            break
        for linkedPhrase, chance in phrases[currentPhrase].iteritems():
            print("Trying {} at {} vs {}...".format(linkedPhrase, chance, random))
            if random <= chance :
                currentPhrase = linkedPhrase
                outputFile.write('|')
                outputFile.write(currentPhrase)
                break
    outputFile.close()
    markovLinksFile.close()

CreateMarkovTune("data/reel/Dmaj/MarkovLinks.txt")
