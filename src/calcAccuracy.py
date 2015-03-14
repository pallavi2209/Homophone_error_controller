import sys
import argparse
import re

def homophAccuracyMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("correctFile")
  parser.add_argument("correctedFile")
  args = parser.parse_args(argv)
  cfileName = args.correctFile
  ctedfileName = args.correctedFile
  myregex = re.compile("\\b(?:it's|its|you're|your|they're|their|loose|lose|to|too)\\b")
  
  cFile = open(cfileName, "r")
  ctedFile = open(ctedfileName, "r")
  cData = cFile.read()
  ctedData = ctedFile.read()

  cmatches = re.finditer(myregex, cData)
  ctedmatches = re.finditer(myregex, ctedData)

  cGroupList = []
  ctedGroupList = []
  for m in cmatches:
    cGroupList.append(m.group())

  for m in ctedmatches:
    ctedGroupList.append(m.group())

  print(str(len(cGroupList)))
  print(str(len(ctedGroupList)))

  totInst = len(cGroupList)
  correctInst = 0
  for i in range(0, len(cGroupList)):
    if cGroupList[i]==ctedGroupList[i]:
      correctInst +=1

  acc = correctInst/totInst
  print(str(acc))






  
  

if __name__=="__main__":
  homophAccuracyMain(sys.argv[1:])


