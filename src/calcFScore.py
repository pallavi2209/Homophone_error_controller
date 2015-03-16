import sys
import argparse
import re

def chckSameGroup(listItem, matchedItem):
  if (listItem == "it's" and matchedItem == "its") or (listItem == "its" and matchedItem == "it's") or (listItem == "you're" and matchedItem == "your") or (listItem == "your" and matchedItem == "you're") or (listItem == "they're" and matchedItem == "their") or (listItem == "their" and matchedItem == "they're") or (listItem == "loose" and matchedItem == "lose") or (listItem == "lose" and matchedItem == "loose") or (listItem == "too" and matchedItem == "to") or (listItem == "to" and matchedItem == "too") or listItem == matchedItem:
    return True
  else:
    return False;


def homophAccuracyMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("incorrectFile")
  parser.add_argument("correctFile")
  parser.add_argument("correctedFile")
  args = parser.parse_args(argv)
  incfileName = args.incorrectFile
  cfileName = args.correctFile
  ctedfileName = args.correctedFile
  myregex = re.compile("\\b(?:it's|its|you're|your|they're|their|loose|lose|to|too)\\b")
  
  cFile = open(cfileName, "r")
  ctedFile = open(ctedfileName, "r")
  incFile  = open(incfileName, "r")
  incData = incFile.read()
  cData = cFile.read()
  ctedData = ctedFile.read()
 
  incmatches =  re.finditer(myregex, incData)
  cmatches = re.finditer(myregex, cData)
  ctedmatches = re.finditer(myregex, ctedData)
 
  incGroupList = []
  cGroupList = []
  ctedGroupList = []
  for m in incmatches:
    incGroupList.append(m.group())

  for m in cmatches:
    cGroupList.append(m.group())

  for m in ctedmatches:
    ctedGroupList.append(m.group())

  totChangesRq = 0
  correctChanges = 0
  totChangesDone = 0
  for i in range(0,len(incGroupList)):
    if not chckSameGroup(incGroupList[i], cGroupList[i]):
      print("not matching")
    if not incGroupList[i] == cGroupList[i]:
      totChangesRq +=1
      if cGroupList[i] == ctedGroupList[i]:
        correctChanges +=1
 
  for i in range(0,len(incGroupList)):
    if not incGroupList[i] == ctedGroupList[i]:
      totChangesDone +=1

  prec = correctChanges/totChangesDone
  recall = correctChanges/totChangesRq

  fscore = (2*prec*recall)/(prec+recall)

  print("Precision:"+str(prec))
  print("Recall:"+str(recall))
  print("F-score:"+ str(fscore))

  totInst = len(cGroupList)
  correctInst = 0
  list_to = ["to", "too"]
  list_thr = ["they're", "their"]
  list_yr = ["you're" , "your"]
  list_lose = ["loose", "lose"]
  list_its = ["its", "it's"]

  c_to = 0
  ct_to =0
  c_thr = 0
  ct_thr = 0
  c_yr = 0
  ct_yr = 0
  c_lose = 0
  ct_lose = 0
  c_its = 0
  ct_its = 0

  totChanges = 0

  for i in range(0, len(cGroupList)):
    if not chckSameGroup(cGroupList[i], ctedGroupList[i]):
      print("not matching")
    if cGroupList[i] == "to" or cGroupList[i] == "too":
      if cGroupList[i]==ctedGroupList[i]:
        c_to +=1
      ct_to +=1
    elif cGroupList[i] == "they're" or cGroupList[i] == "their":
      if cGroupList[i]==ctedGroupList[i]:
        c_thr +=1
      ct_thr +=1
    elif cGroupList[i] == "you're" or cGroupList[i] == "your":
      if cGroupList[i]==ctedGroupList[i]:
        c_yr +=1
      ct_yr +=1
    elif cGroupList[i] == "loose" or cGroupList[i] == "lose":
      if cGroupList[i]==ctedGroupList[i]:
        c_lose +=1
      ct_lose +=1
    elif cGroupList[i] == "it's" or cGroupList[i] == "its":
      if cGroupList[i]==ctedGroupList[i]:
        c_its +=1
      ct_its +=1

    if cGroupList[i]==ctedGroupList[i]:
      correctInst +=1

  acc = correctInst/totInst
  c_to_acc = c_to/ct_to
  c_thr_acc = c_thr/ct_thr
  c_yr_acc = c_yr/ct_yr
  c_its_acc = c_its/ct_its
  c_lose_acc = c_lose/ct_lose

  print("Overall Accuracy:" + str(acc))
  print("acc of to:"+str(c_to_acc))
  print("acc of thr:"+str(c_thr_acc))
  print("acc of your"+str(c_yr_acc))
  print("acc of its:"+str(c_its_acc))
  print("acc of lose:"+str(c_lose_acc))

  print("correct of to/too:"+str(c_to))
  print("total of to/too:"+str(ct_to))
  print("correct of they're/their:"+str(c_thr))
  print("total of they're/their:"+str(ct_thr))
  print("correct of your/you're:"+str(c_yr))
  print("total of your/you're:"+str(ct_yr))
  print("correct of its/it's:"+str(c_its))
  print("total of its/it's:"+str(ct_its))
  print("correct of loose/lose"+str(c_lose))
  print("total of loose/lose"+str(ct_lose))
  
if __name__=="__main__":
  homophAccuracyMain(sys.argv[1:])


