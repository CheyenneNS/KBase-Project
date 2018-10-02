

import urllib.parse 
from collections import defaultdict
from random import choice, shuffle


# Helper functions for reading input file, counting and writing output file.

def readFile(file):
	contents = None

	with open(file, 'r') as fileOpen:
		contents = fileOpen.read().splitlines()
		fileOpen.close()	

		return(contents)

def countLines(file):
	with open(file, 'r') as fileOpen:
		return sum(1 for line in fileOpen)

def writeFile(string):

	File = open("DecodedFrags.txt", "w+")
	File.write(string)
	File.close()

# Helper function for list-string conversion

def toString(List):
	return ''.join(List)



#String assembly functions. The assemble is used when the input file is computationally challenging in its string fragmentation syntex.
# The funcions "listMatch" and overlap are non-computational heavy function used when input files have simple word-based string framentation. 


def assemble(str_list, min=3, max=15):

    if len(str_list) < 2:
        return set(str_list)

    output = set()
    string = str_list.pop()

    for i, match in enumerate(str_list):
        matches = set()

        if match in string:
            matches.add(string)

        elif string in match:
            matches.add(match)

        for n in range(min, max + 1):
            if match[:n] == string[-n:]:
                matches.add(string + match[n:])

            if match[-n:] == string[:n]:
                matches.add(match[:-n] + string)

        for word in matches:
            output.update(assemble(str_list[:i] + str_list[i + 1:] + [word]))

    return(output)



def overlap(string1, string2):

	overlaps = []

	for i in range(len(string2)):
		for j in range(len(string1)):
			if a.endswith(string2[:i + 1], j):
				overlaps.append((i, j))

	return max(overlaps) if overlaps else (0, -1) 

def listMatch(lst):

	overlaps = defaultdict(list)

	while len(lst) > 1:
		overlaps.clear()

		for string1 in lst:
			for string2 in lst:
				if string1 == string2:
					continue

				amount, start = overlap(string1, string2)
				overlaps[amount].append((start, string1, string2))

		maximum = max(overlaps)

		if maximum == 0:
			break

		start, string1, string2 = choice(overlaps[maximum])  
		lst.remove(string1)
		lst.remove(string2)
		lst.append(string1[:start] + string2)

	return(lst)


# Descramble function is the main function used for allocating which string assembly method to use, decoding unfragmented string from url,
# and writing output to file

def descramble(file):

	stringFrag = readFile(file)
	#print(scrambledString)

	if 30 > countLines(file): 

		unscrambledString = list(assemble(stringFrag))
		unfragmentedString = str(unscrambledString[0])

	else:
		unscrambledString = listMatch(stringFrag)
		unfragmentedString = toString(unscrambledString)
		

	
	decodedString = urllib.parse.unquote_plus(unfragmentedString)
	#print(decodedString)
	writenFile = writeFile(decodedString)
	return(writenFile)
	