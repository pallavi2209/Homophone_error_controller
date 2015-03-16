import os
import sys
import argparse
from decimal import Decimal
import copy
import random
import pickle
import re

dictWordClass = {"it's":"c_itis", "its": "c_its", "you're": "c_youre", "your": "c_your", "they're": "c_theyre", "their": "c_their" , "loose": "c_loose" , "lose": "c_lose", "to": "c_to", "too": "c_too"}
listChanged = []

def checkReqContext(pPrev, prev, curr, nxt, nNxt):
  if curr in dictWordClass.keys():
    return dictWordClass[curr]
  else:
    return "NA"

def getClass(resCls):
  if resCls == "c_itis" or resCls == "c_its":
    return set(["c_itis", "c_its"])
  elif resCls == "c_youre" or resCls == "c_your":
    return set(["c_youre", "c_your"])
  elif resCls == "c_theyre" or resCls == "c_their":
    return set(["c_theyre", "c_their"])
  elif resCls == "c_loose" or resCls == "c_lose":
    return set(["c_loose", "c_lose"])
  elif resCls == "c_to" or resCls == "c_too":
    return set(["c_to", "c_too"])

def getWShape(word):
    word = re.sub('[a-z]+','a',word)
    word = re.sub('[A-Z]+','A',word)
    word = re.sub('[0-9]+','9',word)
    word = re.sub('[^0-9a-zA-Z]+','-',word)
    return word

def form_feats_predict(pPrev, prev, curr, nxt, nNxt, dictClsWts):
  resLine = ""
  pPrevW = str(pPrev[0])
  prevW = str(prev[0])
  currW = str(curr[0])
  nxtW = str(nxt[0])
  nNxtW = str(nNxt[0])
  res = checkReqContext(pPrevW, prevW, currW, nxtW, nNxtW)
  if not res == "NA":
    setcls = getClass(res)
    
    f_pPrevW = "PPW:" + pPrevW
    f_prevW = "PW:" + prevW
    f_nxtW = "NW:" + nxtW
    f_nNxtW = "NNW:" +  nNxtW
    f_pPrevTag = "PPT:" + str(pPrev[1])
    f_prevTag = "PT:" + str(prev[1])
    f_nxtTag = "NT:" + str(nxt[1])
    f_nNxtTag = "NNT:" + str(nNxt[1])
    f_prevWSuff = "PWSF:" + prevW[-3:]
    f_nxtWSuff = "NWSF:" + nxtW[-3:]
    f_prevWShape = "PWSH:" + getWShape(prevW)
    f_nextWShape = "NWSH:" + getWShape(nxtW)

    resLine += f_pPrevW + " " +  f_prevW + " " + f_prevWSuff + " " + f_prevWShape + " " + f_nxtW + " "  + f_nxtWSuff + " " + f_nextWShape + " " + f_nNxtW +"\n"

    tokens = resLine.split()
    maxwtcls = max( setcls , key = lambda cls: sum( [ dictClsWts[cls][token] for token in tokens[1:] if token in dictClsWts[cls]]) )
    for k,v in dictWordClass.items():
      if v == maxwtcls:
        predWord = k  
        if currW == predWord:
          listChanged.append((0, predWord))
        else:
          listChanged.append((1, predWord))


def combine_apo_words(wordTagList):
  cWordTagList = []
  prev = wordTagList[0]
  for i in range(1, len(wordTagList)):
    curr = wordTagList[i]
    prevW = prev[0]
    currW = curr[0]
    if (prevW == "it" and currW == "'s") or (prevW == "you" and currW == "'re") or (prevW == "they" and currW == "'re"):
      word = prevW + currW
      tag = prev[1] + "+" + curr[1]
      cWordTagList.pop()
      cWordTagList.append([word,tag])
    else:
      cWordTagList.append(wordTagList[i])
    prev = curr
  return cWordTagList


def classify_and_correct(tokenList, dictClsWts):
  pPrev = (u'BBOS', u'BBOS')
  prev = (u'BOS', u'BOS')
  curr = tokenList[0]
  nxt = tokenList[1]

  for i in range(1,len(tokenList)-2):
    nNxt = tokenList[i]
    form_feats_predict(pPrev, prev, curr, nxt, nNxt, dictClsWts)
    pPrev = prev
    prev = curr
    curr = nxt
    nxt = nNxt
  nNxt = (u'EOS', u'EOS')
  form_feats_predict(pPrev, prev, curr, nxt, nNxt, dictClsWts)
  pPrev = prev
  prev = curr
  curr = nxt
  nxt = nNxt
  nNxt = (u'EEOS', u'EEOS')

  form_feats_predict(pPrev, prev, curr, nxt, nNxt, dictClsWts)

def chckSameGroup(listItem, matchedItem):
  if (listItem == "it's" and matchedItem == "its") or (listItem == "its" and matchedItem == "it's") or (listItem == "you're" and matchedItem == "your") or (listItem == "your" and matchedItem == "you're") or (listItem == "they're" and matchedItem == "their") or (listItem == "their" and matchedItem == "they're") or (listItem == "loose" and matchedItem == "lose") or (listItem == "lose" and matchedItem == "loose") or (listItem == "too" and matchedItem == "to") or (listItem == "to" and matchedItem == "too") or listItem == matchedItem:
    return True
  else:
    return False;

def homophClassifyMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("intaggedFile")
  parser.add_argument("modelFile")
  parser.add_argument("inRawFile")
  parser.add_argument("outFile")
  args = parser.parse_args(argv)
  inTaggedFileName = args.intaggedFile
  mdfname=args.modelFile
  inRawFileName = args.inRawFile
  outFileName = args.outFile

  with open(mdfname,"rb") as handle:
    data=pickle.load(handle)

  dictClsWts=data["wDict"]
  handle.close()

  inTaggedFile  = open(inTaggedFileName, "r")
  wordLines = inTaggedFile.readlines()
  wordTagList = []
  for line in wordLines:
    l = line.split("\t")
    if len(l)>=3:
      word = l[0]
      tag = l[2]
      wordTagList.append([word,tag])
  cWordTagList = combine_apo_words(wordTagList)
  classify_and_correct(cWordTagList, dictClsWts)
 
  myregex = re.compile("\\b(?:it's|its|you're|your|they're|their|loose|lose|to|too)\\b")
  
  rawFile = open(inRawFileName, "r")
  data = rawFile.read()
  matchCount = len(re.findall(myregex, data))
  matches = re.finditer(myregex, data)
  idxChangeList = 0
  try:
    os.remove(outFileName)
  except OSError:
    pass
  outfile = open(outFileName,"a")
  iPrevEnd = 0
  for match in matches:
    ifSame = chckSameGroup(listChanged[idxChangeList][1],match.group())
    if ifSame == False:
      continue;
    elif data[match.start()-1]=="-":
      idxChangeList +=1
      continue; 
    if (not listChanged[idxChangeList][0]==0):
      istart = match.start()
      outfile.write(data[iPrevEnd:istart])
      outfile.write(listChanged[idxChangeList][1])
      iPrevEnd = match.end()
    idxChangeList +=1
  outfile.write(data[iPrevEnd:])
    
  inTaggedFile.close()
  rawFile.close()
  outfile.close()  

if __name__=="__main__":
  homophClassifyMain(sys.argv[1:])
