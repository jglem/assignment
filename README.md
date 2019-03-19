## C-I-S-C-O assignment

This is a recruiting assignment for C-I-S-C-O by Justina L.
The code is written in python 3.6.7, but python 3.7.1 works as well and possibly other versions of python 3. It takes the JSON file to parse as the first argument after the file name in command line.

Ex. "python3 assignment.py log.json" or "python3 assignment.py <path to file from current directory>"

Assumptions:
1. The valid types for each field are based on the example json file sent in the assignment email.
ts: integer
pt: integer
si: string
uu: string
bg: string
sha: string
nm: string
ph: string
dp: integer

2. Each entry in the JSON file is on a single line, which is the format of the example json file sent in the assignment email.
3. As observed in the example json file, the filename found in the path field ("ph") should be the same as the name found in the name field ("nm").
Ex. Both "nm":"ywcgdssxa.qxd","ph":"/dabs/yuqqwzxq/nvwmsndab/veottijas/ywcgdssxa.qxd" and "nm":"dpxjbt.cvs","ph":"dpxjbt.cvs" are valid pairs of json data.
This filtering can be turned off in the command line by typing "pathCheckOff" as the second argument.
Ex. "python3 assignment.py log.json pathCheckOff" If no second argument is offered or the second argument is not "pathCheckOff", the filename in the "ph" is checked against the "nm" field.
