import re
import numpy as np
import urllib.parse 

#METHOD 1

# Helper functions for reading into text and writing output text file

def readFile(file):
	contents = None

	with open(file, 'r') as fileOpen:
		contents = fileOpen.read().splitlines()
		fileOpen.close()

		return(contents)

def writeFile(string):

	File = open("Unfragmented.txt", "w+")
	File.write(string)
	File.close()

# The following functions arrange strings into the nescessary struct to be input
# Into the Hamiltonian Path Finder


# First action taken to finding Hamiltonian paths in string fragments puting all fragments into
# a simple dictionary such that each fragment can be appended with the values of it matches

def makeDictionary(arr_frags):
	my_map = {}

	for string in arr_frags:
		my_map.setdefault(string, [])
	return(my_map)

# Possible Fragment matches are put into a matching list

def makeMatchingList(arr_frags, string):

	match_list = []
	
	for candidate in arr_frags:
		substring = string[-3:]
		if substring in candidate and candidate != string:
			match_list.append(candidate)

	return(match_list)

# The function assemble creates a graph/dictionary for each strings matching list
# Only choosing the best matches - matches that contain the last 3-14 values of the ending fragment	

def assemble(arr_frags, my_dict, min=3, max=14):

	for string in arr_frags:

		matching_list = makeMatchingList(arr_frags, string)
		#print(matching_list)

		for match in matching_list:
			#print(match)
			for n in range(min, max + 1):
				if match[:n] == string[-n:]:
					my_dict[string].append(match)
					#my_dict[match].append(string)
	
	return(my_dict)

#Hamiltonian Path Finder Functions 
#http://www.python.org/doc/essays/graphs/

def find_all_paths(graph, start, end, path=[]):
	
	path = path + [start]

	if start == end:
		return [path]

	if not start in graph:
		return []
	paths = []

	for node in graph[start]:
		if node not in path:
			newpaths = find_all_paths(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)

	return paths

def find_paths(graph):

	cycles=[]
	for startnode in graph:
		for endnode in graph:
			newpaths = find_all_paths(graph, startnode, endnode)
			for path in newpaths:
				if (len(path)==len(graph)):
					cycles.append(path)

		return cycles

print("Finding Hamiltonian Paths----")

# Function descramble connects all methods and outputs a written text file 
# Idealy with the unfragmented strings 


def descramble(file):

	arr_Frags = np.asarray(readFile(file))
	Dictionary = makeDictionary(arr_Frags)
	#print(Dictionary)
	

	graph = assemble(arr_Frags, Dictionary)
	writenFile = writeFile(str(graph))
	return writenFile
	#print(graph)

	#path = find_paths(graph)
	#return(path)

	#stringPaths = find_paths(matching_dict)
	#mostlikelystring = stringPaths[0]
	#for string in stringPaths:
		#stringPathn = ''.join(string)
		#decodedString = urllib.parse.unquote_plus(stringPathn)

	#print(stringPaths)

	#print(matching_dict)