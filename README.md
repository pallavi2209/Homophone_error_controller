I have tried two approaches for this assignment:
1. Classification (Successful)
2. Language model (Unsuccessful)

###CLASSIFICATION approach:
In classification model, I have tried to use perceptron to train features around the word I have to correct. I have approached this task as "fill in the blank" task. I take the context around the blank and have tried to fill in that blank by training my perceptron on features of that conte
xt.

Data Sources:
- Brown corpus from http://www.nltk.org/nltk_data/
- Project Gutenberg Selections from http://www.nltk.org/nltk_data/
- Sentiment data from CSCI544 Homework 1
- Tagged data from CSCI544 Homeowork 2

Steps in Clasification and data correction:
1. POS tag data
I used ClearNLP Part-of-Speech Tagger availaible at http://clearnlp.wikispaces.com/posTagger to tag the collected data.
Command used: java -XX:+UseConcMarkSweepGC -Xmx1g com.clearnlp.nlp.engine.NLPDecode -z pos -c config_en_pos.xml -i <data-file> -oe pos
Output: POS tagged file
Example: brown.txt.pos

2. Create feature file
Using createHomophFeat.py (submitted in src), I created feature file to be used by perceptron for learning feature weights. I tried different combinations of following features:
Previous to previous word (PPW), Previous to previous POS tag (PPT), Previous word (PW), Previous POS tag (PT), Previous word suffix (PWSF), Previous word shape (PWSH), Next to next word (NNW), Next to next POS tag (NNT), Next word (NW), Next POS tag (NT), Next word suffix (NWSF), Next word shape (NWSH).

Command: python3 createHomophFeat.py [POS_tagged_file] [tagged_file_type] [feature_file]
POS_tagged_file: output from clearNLP or pos.train file from HW2
tagged_file_type: slash (if pos.train)
                  clearNLP (if clearNLP tagged file)
feature_file: output file (gets appended in each run)

Examples:
python3 createHomophFeat.py pos.train slash in.percept.feat
python3 createHomophFeat.py brown.txt.pos clearNLP in.percept.feat
python3 createHomophFeat.py gutenbergAllRaw.txt.pos clearNLP in.percept.feat
python3 createHomophFeat.py sentTrainingPure.pos clearNLP in.percept.feat
python3 createHomophFeat.py sentDevPure.pos clearNLP in.percept.feat
python3 createHomophFeat.py sentTestPure.pos clearNLP in.percept.feat

Output: in.percept.feat with features from all the files above.

python3 createHomophFeat.py hw3.dev.txt.pos clearNLP hw3.dev.feat
Output: hw3.dev.feat , dev file features to be used in Step 3.

3. Train perceptron
I used the perceptron oh HW2 to train my features
Command: python3 perceplearn.py [feature_file] [output_model] -h [dev_file]
feature_file: output file from Step 2.
output_model: output of this run
dev_file: Optional. To test model in each iteration and pick best one.

Example: python3 perceplearn.py in.percept.feat homoph.model -h hw3.dev.feat
Output: Prints accuracy in each iteration and saves model file with max accuracy.

4. Apply model and correct errors in file.
Using homophCorrect.py (submitted in src), I correct the error file using the model fom Step 3.

Command: python3 homophCorrect.py [tagged_errored_input_file] [perceptron_model] [errored_input_file] [corrected_output_file]
tagged_errored_input_file: error file tagged using clearNLP
perceptron_model: model formed from perceptron training
errored_input_file: error file given
corrected_output_file: corrected error file, which is submitted

Example:
python3 homophCorrect.py hw3.dev.err.txt.pos homoph.model hw3.dev.err.txt hw3.devoutput.txt
python3 homophCorrect.py hw3.test.err.txt.pos homoph.model hw3.test.err.txt hw3.output.txt

5. Calculate accuracy
I calculate accuracy on dev data using calcFScore.py (submitted in src)
Command: python3 calcFScore.py [incorrect_file] [correct_file] [corrected_output_file]
Example: python3 calcFScore.py hw3.dev.err.txt hw3.dev.txt hw3.devoutput.txt

Results (Refer Step 2. for full feature names and details):
Features:
Previous to previous word (i-2 word),
Previous to previous POS tag (i-2 tag),
Previous word (i-1 word),
Previous POS tag (i-1 tag),
Previous word suffix (i-1 suffix),
Previous word shape (i-1 shape),
Next to next word (i+2 word),
Next to next POS tag (i+2 tag),
Next word (i+1 word),
Next POS tag (i+1 tag),
Next word suffix (i+1 suffix),
Next word shape (i+1 shape).

Try 1: Features Used - All features : i-2 word, i-2 tag, i-1 word, i-1 tag, i-1 suffix, i-1 shape, i+2 word, i+2 tag, i+1 word, i+1 tag, i+1 suffix, i+1 shape
Result F-Score: 0.906113

Try 3:  Features used - All without i-2 and i+2 POS tags: i-2 word, i-1 word, i-1 tag, i-1 suffix, i-1 shape, i+2 word, i+1 word, i+1 tag, i+1 suffix, i+1 shape
Result F-Score: 0.924622
Tells us: i-2 and i+2 tags doing harm, remove them

Try 2: Features used - All without i-2 and i+2 features: i-1 word, i-1 tag, i-1 suffix, i-1 shape, i+1 word, i+1 tag, i+1 suffix, i+1 shape
Result F-Score: 0.87563
Tells us: i-2 and i+2 features helping

Try 2: Features used - All without i-2 and i+2 features and no POS tags : i-1 word, i-1 suffix, i-1 shape, i+1 word, i+1 suffix, i+1 shape
Result F-Score: 0.93675
Hint: POS tags are not favoured

Try 3: Features used - All without POS tags : i-2 word, i-1 word, i-1 suffix, i-1 shape, i+2 word, i+1 word, i+1 suffix, i+1 shape
Result F-Score: 0.98616

Using POS tags as features give good F-Score (~98%) on correct file, but reduces accuracy on errored file by around 7-8%. One reason for this can be, incorrect tags predicted by clearNLP because of incorrect words in error file. So, I decided not to use POS tags as features.

#####Final features used:
Previous to previous word (i-2 word),
Previous word (i-1 word),
Previous word suffix (i-1 suffix),
Previous word shape (i-1 shape),
Next to next word (i+2 word),
Next word (i+1 word),
Next word suffix (i+1 suffix),
Next word shape (i+1 shape).

Precision: 0.97972
Recall: 0.99270
F-Score: 0.98616


###LANGUAGE MODEL approach:
I decide to try CMU Language model toolkit available at http://www.speech.cs.cmu.edu/SLM/toolkit.html.

Data Source: I downloaded wikipedia dump from http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 and extracted plain text from this using techniques given on this article: http://trulymadlywordly.blogspot.com/2011/03/creating-text-corpus-from-wikipedia.html

It gave me segmentation fault when I tried to make a vocabulary out of wikipedia dump using command as follows:
cat WikiDataDump.txt | CMU-Cam_Toolkit_v2/bin/text2wfreq | CMU-Cam_Toolkit_v2/bin/wfreq2vocab > wiki.vocab
>> Segmentation fault

I tried on lesser data and it worked fine. I mad language model and calculated probabilties of n grams in test data using the commands:
cat lessWikiDataDump.txt | CMU-Cam_Toolkit_v2/bin/text2idngram -temp . -vocab lwiki.vocab > lwiki.idngram
cat lessWikiDataDump.txt | CMU-Cam_Toolkit_v2/bin/text2idngram -temp . -vocab lwiki.vocab | CMU-Cam_Toolkit_v2/bin/idngram2lm -vocab lwiki.vocab -idngram - -binary lwiki.binlm
But, I could not get good results using these probablities. The reason I suppose was lesser data as language model requires large data for good results. And my system was not able to handle large data.
So, I decided to go with Classification approach as described before.



