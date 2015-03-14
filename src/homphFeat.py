import sys
#sys.path.append('..')
import argparse
import re
import os
import tempfile
import pickle
try:
  import perceplearn
except:
  print("Cannot find perceplearn module. Please check directory structure.\n Exiting... ")
  sys.exit()

def getWShape(word):
    word = re.sub('[a-z]+','a',word)
    word = re.sub('[A-Z]+','A',word)
    word = re.sub('[0-9]+','9',word)
    word = re.sub('[^0-9a-zA-Z]+','-',word)
    return word

def checkReqContext(pPrev, prev, curr, nxt, nNxt):
  if curr == "it's" or curr == "itis":
    return "c_itis"
  elif curr == "its":
    return "c_its"
  elif curr == "you're" or curr == "youare":
    return "c_youre"
  elif curr == "your":
    return "c_your"
  elif curr == "they're" or curr == "theyare":
    return "c_theyre"
  elif curr == "their":
    return "c_their"
  elif curr == "loose":
    return "c_loose"
  elif curr == "lose":
    return "c_lose"
  elif curr == "to":
    return "c_to"
  elif curr == "too":
    return "c_too"
  else:
    return "NA"

def form_feats_writeToFile(pPrev, prev, curr, nxt, nNxt, outfile):
  resLine = ""
  pPrevW = str(pPrev[0])
  prevW = str(prev[0])
  currW = str(curr[0])
  nxtW = str(nxt[0])
  nNxtW = str(nNxt[0])

  res = checkReqContext(pPrevW, prevW, currW, nxtW, nNxtW)
  if not res == "NA":
    resLine = resLine + res
    f_pPrevW = "PPW:" + pPrevW
    f_prevW = "PW:" + prevW
    #f_currW = "CW:" + str(curr[0])
    f_nxtW = "NW:" + nxtW
    f_nNxtW = "NNW:" +  nNxtW
    f_pPrevTag = "PPT:" + str(pPrev[1])
    f_prevTag = "PT:" + str(prev[1])
    #f_currTag = "CT:" + str(curr[1])
    f_nxtTag = "NT:" + str(nxt[1])
    f_nNxtTag = "NNT:" + str(nNxt[1])
    f_prevWSuff = "PWSF:" + prevW[-3:]
    f_nxtWSuff = "NWSF:" + nxtW[-3:]
    resLine += " " + f_pPrevW + " " + f_pPrevTag + " " + f_prevW + " " + f_prevTag + " " + f_prevWSuff + " " + f_nxtWSuff + " " + f_nxtW + " " + f_nxtTag + " " + f_nNxtW + " " + f_nNxtTag + "\n"

    outfile.write(resLine)


def createperceptFile(tokenList,outFileName):
  outfile = open(outFileName, "a")
  pPrev = (u'BBOS', u'BBOS')
  prev = (u'BOS', u'BOS')
  curr = tokenList[0]
  nxt = tokenList[1]

  for i in range(1,len(tokenList)-2):
    nNxt = tokenList[i]
    form_feats_writeToFile(pPrev, prev, curr, nxt, nNxt, outfile)
    pPrev = prev
    prev = curr
    curr = nxt
    nxt = nNxt
  nNxt = (u'EOS', u'EOS')
  form_feats_writeToFile(pPrev, prev, curr, nxt, nNxt, outfile)
  pPrev = prev
  prev = curr
  curr = nxt
  nxt = nNxt
  nNxt = (u'EEOS', u'EEOS')
  
  form_feats_writeToFile(pPrev, prev, curr, nxt, nNxt, outfile)  
  
  outfile.close()

def combine_apo_words(wordTagList):
  cWordTagList = []
  prev = wordTagList[0]
  for i in range(1, len(wordTagList)):
    curr = wordTagList[i]
    prevW = prev[0]
    currW = curr[0]
    if (prevW == "it" and currW == "'s") or (prevW == "it" and currW == "is") or (prevW == "you" and currW == "'re") or (prevW == "you" and currW == "are") or (prevW == "they" and currW == "'re") or (prevW == "they" and currW == "are"):
      word = prevW + currW
      tag = prev[1] + "+" + curr[1]
      cWordTagList.pop()
      cWordTagList.append([word,tag])
    else:
      cWordTagList.append(wordTagList[i])
    prev = curr
  return cWordTagList

def handleSlashTagged(infname, outfname):
  infile = open(infname, "r")
  data = infile.read()
  taggedtokens = data.split()
  wordTagList = map(lambda x : x.split("/"), taggedtokens)
  cWordTagList = combine_apo_words(list(wordTagList))
  createperceptFile(cWordTagList, outfname)

def handleClearNLPTagged(infname, outfname):
  infile = open(infname, "r")
  dataLines = infile.readlines()
  wordTagList = []
  for line in dataLines:
    l = line.split("\t")
    if len(l)>=3:
      word = l[0]
      tag = l[2]
      wordTagList.append([word,tag])
  cWordTagList = combine_apo_words(wordTagList)
  createperceptFile(cWordTagList, outfname)


def homoPostrainMain(argv):
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument("taggedfile")
  parser.add_argument("taggedType")
  parser.add_argument("outfile")
  args = parser.parse_args(argv)
  taggedfname=args.taggedfile
  tagtype = args.taggedType
  outfname = args.outfile

  if tagtype == "slash":
    handleSlashTagged(taggedfname, outfname)
  elif tagtype == "clearNLP":
    handleClearNLPTagged(taggedfname, outfname)

if __name__=="__main__":
  homoPostrainMain(sys.argv[1:])
