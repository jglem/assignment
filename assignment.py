import sys

#Open JSON file
try:
	fileHandle = open(sys.argv[1], "r")
except IOError:
	print ("Could not open file ", sys.argv[1], " for reading.")

#Create a dictionary for extensions
extensions = {}

#Create an array with expected substrings per line in the JSON file
formatNames = ["\"ts\"", ",\"pt\"", ",\"si\"", ",\"uu\"", ",\"bg\"", ",\"sha\"", ",\"nm\"", ",\"ph\"", ",\"dp\""]

#Parsing though each line:
for line in fileHandle:
	#Assume line is valid initially
	validLine = True
	#Check if each substring in formatNames is found in the line
	for fNames in formatNames:
		#If the substring is not found, the line is not valid, break
		if fNames not in line:		
			validLine = False
			break
			
	#If line is not valid, continue to next line in JSON line
	if validLine == False:
		print("invalid line: "+line)
		continue
	
	#Find the index where the file name information is
	nameIndex = line.find(",\"nm\":")
	
	#Create a substring starting from the filename to the end of the line to the second
	#quotation mark in the "nm" entry
	fileName = line[nameIndex+7:]
	fileName = fileName[0:fileName.find("\"")]
	#print (fileName)
	#Find the first dot found in the filename. This will help account for files with extesions (.tar.gz)
	dotIndex = fileName.find(".")
	#print(dotIndex)
	
	#If no dot is found, this is a file without an extension
	if (dotIndex == -1):
		#If there is not a "none" entry in the extensions dictionary
		if "none" not in extensions:
			#Make a "none" entry and set it to an empty dictionary
			extensions["none"] = {}
			#Inside that nested entry, record an entry for the filename
			extensions["none"][fileName] = 1
		else:
			#If there is an entry for "none" in extensions, see if fileName is found in the "none" dictionary
			if fileName not in extensions["none"]:
				#If not found in the "none" dictionary, add the fileName as a new entry
				extensions["none"][fileName] = 1
			else:
				#fileName entry is found in the "none" dictionary
				print("Double found! " + fileName)

	#If a dot is found in the fileName
	else:
		#Separate the extension name from the just the filename
		extName = fileName[dotIndex+1:]
		fileName = fileName[0:dotIndex]
		#print(fileName)
		#print(extName)
		#If the extName is not an entry in the extensions dictionary
		if extName not in extensions:
			#Make an entry for extName and set it to an empty dictionary
			extensions[extName] = {}
			#Add the fileName as an entry in the new empty dictionary for extName
			extensions[extName][fileName]=1
		
		#If the extName has an entry in the extensions dictionary
		else:
			#If the fileName is not found in the nested extName dictionary
			if fileName not in extensions[extName]:
				#Add fileName as a new entry in the nested extName dictionary
				extensions[extName][fileName]=1
			
			else:
				#fileName entry is found in the nested extName dictionary
				print("Double found! " + fileName +"."+extName)
				continue

sum=0
#Print results
print("Results:")
for element in extensions:

	print(element+": "+str(len(extensions[element])))
	sum+= len(extensions[element])

print("total: "+str(sum))
		

	
	
