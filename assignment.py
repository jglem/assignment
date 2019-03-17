import sys, json

#Open JSON file
try:
	fileHandle = open(sys.argv[1], "r")
except IOError:
	print ("Could not open file ", sys.argv[1], " for reading.")
except IndexError:
	print ("No argument was given for filename. Try again with filename added. \nEx. \"python3 assignment.py log.json\" or \"python3 assignment.py <path to file>\"")
	sys.exit()

#Create a dictionary for extensions
extensions = {}

#Create an array with expected substrings per line in the JSON file
entryNames = ["ts", "pt", "si", "uu", "bg", "sha", "nm", "ph", "dp"]

#Parsing though each line:
for line in fileHandle:
	#Assume line is valid initially
	validLine = True
	
	#Load json data
	#If line is not in JSON format, catch the exception from loading and flag the line as invalid
	try:
		data = json.loads(line)
	except:
		validLine = False

	#If the JSON data was loaded, make sure each entry name is found in the JSON data
	if validLine is not False:
		for eName in entryNames:
			
			#If the entry name is not found, the line is not valid, break
			if eName not in data:		
				validLine = False
				print("Missing: "+eName)
				break

			#Make sure none of the entries have types that are not int nor string. 
			#This makes sure there are no nested json entries inside of the fields
			#Ex. {"address": {"street":123, cat:"meow"}}
			if not isinstance(data[eName],int) and not isinstance(data[eName],str):
				validLine = False
				print("Field is not str or int")
				break
				
			#Check that for each entry, the given field is the right type
			if (eName == "ts" or eName == "pt" or eName == "dp") and not isinstance(data[eName], int):
				validLine = False
				print(eName+" has field that is not int")
				break
			elif (eName == "si" or eName == "uu" or eName == "bg" or eName == "sha" or eName == "nm" or eName == "ph") and not isinstance(data[eName],str):
				validLine = False
				print(eName+" has field that is not str")
				break
			
			#If fName is "dp", check if the dp value is valid
			if eName == "dp":
				#Get the dpValue
				dpValue = data[eName]
				print("dpValue: "+str(dpValue))
				
				#If the dpValue is not 1,2, or 3, the line is invalid
				if int(dpValue) < 1 or int(dpValue) > 3:
					validLine = False
					break
				
	#If line is not valid, continue to next line in JSON file
	if validLine == False:
		print("invalid line: "+line)
		continue
	

	#Retrieve filename from nm field
	fileName = data["nm"]

	#print (fileName)
	#Find the first dot found in the filename. This will help account for files with extesions (.tar.gz)
	dotIndex = fileName.find(".")
	#print(dotIndex)
	
	#If no dot is found, this is a file without an extension
	if (dotIndex == -1):
		#If there is not a "No extension" entry in the extensions dictionary
		if "No extension" not in extensions:
			#Make a "No extension" entry and set it to an empty dictionary
			extensions["No extension"] = {}
			#Inside that nested entry, record an entry for the filename
			extensions["No extension"][fileName] = 1
		else:
			#If there is an entry for "No extension" in extensions, see if fileName is found in the "No extension" dictionary
			if fileName not in extensions["No extension"]:
				#If not found in the "No extension" dictionary, add the fileName as a new entry
				extensions["No extension"][fileName] = 1
			else:
				#fileName entry is found in the "No extension" dictionary
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
if len(extensions) > 0:
	for element in extensions:

		print(element+": "+str(len(extensions[element])))
		sum+= len(extensions[element])
else:
	print("No valid lines found in file")

print("total: "+str(sum))
		

	
	
