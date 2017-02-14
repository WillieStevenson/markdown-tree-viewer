#!/usr/bin/python

##
#
# A python/broswer based tree generator
#
# Author: Willie Stevenson
#
##

# Extract level and node value from current line
# of input file
# ----------------------------------------------
# Levels are indicated by the - mark. The root
# node has no - mark.
def countLevelAndExtractNodeVal(line):
	level = 0
	nodeVal = ""

	for c in line:
		if c == "-":
			level = level + 1
		else:
			nodeVal = nodeVal + c
	
	return [level, nodeVal[:-1]]

# Checks if the given input file is valid graph
# ---------------------------------------------
# A valid graph is a graph where the first node 
# is a root node and is the only root node.
# Additionaly, a next node cannot have a
# level greater than 1 more than the
# level found at the previous node. 
def checkInputGraphValidity(INPUT_FILE):
	count = 1
	rootNodeCount = 0
	previousNodeLevel = 0

	file = open(INPUT_FILE)

	for line in file:

		level, nodeVal = countLevelAndExtractNodeVal(line)

		if level == 0:
			rootNodeCount = rootNodeCount + 1
		if rootNodeCount != 1:
			print "Either no root nodes are present or their was more than one root node found in the input file."
			exit()
		if level - previousNodeLevel > 1:
			print "Input graph invalid. Invalid node %s found at line %d in inupt file." % (nodeVal, count)
			exit()

		previousNodeLevel = level
		count = count + 1

	file.close()

# Generates valid input data to display as tree
# ---------------------------------------------
# Data is written to an input file. Tree output
# is only generated when -g command is passed
# with commands for generating tree data.
def dataGen(nodes, maxLevelDepth):
	import random

	nodeList = range(nodes)

	file = open("input", "w")
	file.write(str(nodeList[0]) + "\n")
	file.write("-" + str(nodeList[1]) + "\n")

	currentLevel = 1

	for i in nodeList[2:]:
		level = random.randint(1, maxLevelDepth)

		while level > currentLevel + 1:
			level = random.randint(1, maxLevelDepth)

		tempString = ""

		for j in range(level):
			tempString = tempString + "-"

		tempString = tempString + str(nodeList[i]) + "\n"

		file.write(tempString)

		currentLevel = level
		tempString = ""

# Generates output data to display as tree
# ----------------------------------------
# Input file is read and json data is 
# generated to view tree through
# web browser. 
def outputGen():
	import ast
	import json

	INPUT_FILE = "input"

	checkInputGraphValidity(INPUT_FILE)

	treeString = ""
	previousNodeLevel = 0

	file = open(INPUT_FILE)

	for line in file:

		level, nodeVal = countLevelAndExtractNodeVal(line)

		if level == 0:
			treeString = treeString + "[{'name':'" + nodeVal + "','children':["
		if level > 0:
			if level - previousNodeLevel == 1:
				treeString = treeString + "{'name':'" + nodeVal + "','children': ["
			if level - previousNodeLevel == 0:
				treeString = treeString + "]},{'name':'" + nodeVal + "','children': ["
			if level - previousNodeLevel < 0:
				count = previousNodeLevel - level

				if count == 1:
					treeString = treeString + "]}]},{'name':'" + nodeVal + "','children': ["
				else:
					for i in range(count + 1):
						treeString = treeString + "]}"
					treeString = treeString + ",{'name':'" + nodeVal + "','children': ["

		previousNodeLevel = level

	file.close()

	for i in range(level + 1):
		treeString = treeString + "]}"

	treeString = treeString + "]"

	file = open("output.json", 'w')
	file.write(json.dumps(ast.literal_eval(treeString)))



if __name__ == "__main__":
	import getopt
	import sys

	nodes = 0
	maxLevelDepth = 0
	switch1, switch2, switch3 = False, False, False

	try:
		opts, args = getopt.getopt(sys.argv[1:], "n:l:gh", ["nodes=", "level=", "generate=","help"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print(err) # will print something like "option -a not recognized"
		sys.exit(-1)

	for o, a in opts:
		if o in ("-n", "--nodes"):
			nodes = int(a)
			switch1 = True
		elif o in ("-l", "--max-level-depth"):
			maxLevelDepth = int(a)
			switch2 = True
		elif o in ("-g", "--generate-tree-output"):
			switch3 = True
		elif o in ("-h", "--help"):
			print """
Generate a tree from simple input to view in the browser.

Usage:
	$ tree-gen -n (int > 1) -l (int > 1) [-g]


-h, --help                     See usage

Generate Input Data
--------------------------------------------------
-n, --node                     Number of nodes in tree
-l, --max-level-depth          Max number of levels that could be in the tree

Generate Output Tree Data
--------------------------------------------------
-g, --generate-tree-output     Generate tree JSON output

			"""
			sys.exit()
		else:
			assert False, "Unhandled option"
			sys.exit(-1)

	if len(sys.argv) < 2:
		print 'See usage with -h or --help'
		sys.exit()

	if switch1 and switch2 and switch3:
		dataGen(nodes, maxLevelDepth)
		outputGen()
	elif switch1 and switch2:
		dataGen(nodes, maxLevelDepth)
	elif switch1 == False and switch2 == False and switch3 == True:
		outputGen()