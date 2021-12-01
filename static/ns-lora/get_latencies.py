import csv
import sys

filepath = sys.argv[1]

dict = []

with open(filepath) as fp:
   line = fp.readline()
   while line:
       words = line.split()
       id = words[len(words)-1].replace(')', '')
       if "EndDeviceLorawanMac:Send(" in line:
           start = float(words[0].replace('s', '').replace('+', ''))
           element = {"_id": id, "start": start, "end": ""}
           dict.append(element)
           line = fp.readline()
       else:
           id = words[len(words)-1].replace(')', '')
           end = float(words[0].replace('s', '').replace('+', ''))
           line = fp.readline()
           for element in dict:
               if element["_id"] == id:
                   start = element["start"]
                   break

print ("{:.4f}".format(end-start))