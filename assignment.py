#Name: Justina L.
#C-I-S-C-O assignment
import sys, json

#Initialize pathCheck boolean, which determines if the filename 
#in the "ph" field is checked with the "nm" field
pathCheck = True

#Check the command line to see if path check should be turned off
try:
	if sys.argv[2] == "pathCheckOff":
		pathCheck = False
		print("Path check turned off")
except:
	pass
	

#Open JSON file
try:
	fileHandle = open(sys.argv[1], "r")
except IOError:
	print ("Could not open file ", sys.argv[1], " for reading.")
except IndexError:
	print ("No argument was given for filename. Try again with filename added. \nEx. \"python3 assignment.py log.json\" or \"python3 assignment.py <path to file from directory holding assignment.py>\"")
	sys.exit()

#Create a dictionary for extensions
extensions = {}

#Create an array with expected field names per line in the JSON file
fieldNames = ["ts", "pt", "si", "uu", "bg", "sha", "nm", "ph", "dp"]

#Parsing though each line:
for line in fileHandle:
	
	#Assume line is valid initially
	validLine = True
	
	#Load json data
	#If line is not in proper JSON format, catch the exception from loading and flag the line as invalid
	try:
		data = json.loads(line)
	except:
		validLine = False
		
	#########Check to see the given JSON data is valid#########
	#If the JSON data was loaded, perform validity checks on the JSON data
	if validLine is not False:
		
		#For each expected field name
		for fName in fieldNames:
			
			#1) Check if the field name is found in the loaded JSON data
			if fName not in data:		
				validLine = False
				break
				
			#2) Check that for each field, the given field is the right data type
			if (fName == "ts" or fName == "pt" or fName == "dp") and not isinstance(data[fName], int):
				validLine = False
				break
			elif (fName == "si" or fName == "uu" or fName == "bg" or fName == "sha" or fName == "nm" or fName == "ph") and not isinstance(data[fName],str):
				validLine = False
				break
			
			#3) If path check is turned on and the current fName is "ph"
			#check the filename in "ph" against the "nm" field
			if pathCheck and fName == "ph":
				
					#Find the index where the last '/' is
					slashIndex = data[fName].rfind("/")
					pathFileName = ""
					
					#If a slash was found,
					#create substring consisting of everything after that last '/'
					if slashIndex > -1:						
						pathFileName = data[fName][slashIndex+1:]
						
					#else, the path is just the filename
					else:
						pathFileName = data[fName]
					
					#If the filenames do not match, the line is not valid
					if pathFileName != data["nm"]:
						validLine = False
						break
			
			#4) If fName is "dp", check if the dp value is valid,
			#get the dp value
			if fName == "dp":				
				dpValue = data[fName]
				
				#If the dpValue is not 1,2, or 3, the line is invalid
				if int(dpValue) < 1 or int(dpValue) > 3:
					validLine = False
					break
				
	#If line is not valid, continue to the next line in the JSON file
	if validLine == False:
		continue
	
	#########Record unique filenames into a set of nested dictionaries#########	
	#Retrieve filename from nm field
	fileName = data["nm"]

	#Find the first dot found in the filename. This will help account for files with extensions (.tar.gz)
	dotIndex = fileName.find(".")
	
	#If no dot is found, this is a file without an extension
	if (dotIndex == -1):
		
		#If there is not a "No extension" entry in the extensions dictionary,
		#make a "No extension" entry and set it to an empty dictionary,
		if "No extension" not in extensions:			
			extensions["No extension"] = {}

		#If fileName is not found in the "No extension" dictionary,
		#add a new entry in the "No extensions" dictionary for fileName
		if fileName not in extensions["No extension"]:
			extensions["No extension"][fileName] = 1
			
		#else, do not try to add anything new to the "No extensions" dictionary

	#If a dot is found in the fileName, this is a filename with an extension
	else:
		
		#Separate the extension name from the just the filename
		extName = fileName[dotIndex+1:]
		fileName = fileName[0:dotIndex]

		#If the extName is not an entry in the extensions dictionary,
		#make an entry for extName and set it to an empty dictionary
		if extName not in extensions:			
			extensions[extName] = {}			

		#If the fileName is not found in the nested extName dictionary,
		#add fileName as a new entry in the nested extName dictionary
		if fileName not in extensions[extName]:				
			extensions[extName][fileName]=1
			
		#else, fileName entry is found in the nested extName dictionary, do nothing			

#########Print results alphabetically and tally number of unique filenames#########
sum=0
print("Results:")
if len(extensions) > 0:
	for key in sorted(extensions.keys()):
		print(key+": "+str(len(extensions[key])))
		sum+= len(extensions[key])
else:
	print("No valid lines found in file")

print("Total number of unique filenames: "+str(sum))
		

	
	
