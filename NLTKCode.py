import nltk
import csv
from nltk.corpus import stopwords
from urlparse import urlparse
from nltk.collocations import *
from nltk.stem.wordnet import WordNetLemmatizer
import sys
from operator import itemgetter
import json

class autoviv(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# temp = sys.stdout #store original stdout object for later
# sys.stdout = open('/Users/mgoold/Documents/NLTKProject/log.txt','w') #redirect all prints to this log file

nWords=10
puncts='1234557890#{}[].?!,\'\"'

# porter = nltk.PorterStemmer()
lmtzr = WordNetLemmatizer()

DESIRE=['error','problem','suck','issue','broken','wont','dont','cant','hate']
stopwordadditions=['site','hotel','room','review','would','error','problem','suck','issue','broken','wont','dont','cant','hate','hotwire','hotels']
# stopwordadditions=[]
# stopwordadditions=['flight','thi','get','dont']
pageorder=[]
# pageorder=['hotels/results-opaque','hotels/results','hotels/searchResults','hotels/searchResults/sort']
outputlist={}

stem_list=[lmtzr.lemmatize(word) for word in DESIRE]

csvfile=open('/Users/mgoold/Documents/NLTKProject/hotel6.14--6.28.13.txt','rU')

f = csv.reader(csvfile, delimiter='\t', quotechar="'")

stopwordslist=stopwords.words('english')

for i in range(0,len(stopwordadditions)):
  stopwordslist.append(stopwordadditions[i])

mtrx=autoviv() #special class for automatically nesting dictionaries

mtrx['d3layout']='stack'
mtrx['chartsub']='bar'
mtrx['release']='13.08'
mtrx['startdate']='01-APR-2013'
mtrx['enddate']='30-APR-2013'
mtrx['charttitle']='Keyword Counts by Page for Hotel Vertical'
mtrx['chartnote']='{This chart shows keyword counts for comments having negative words: error,problem,suck,issue,broken,wont,dont,cant,hate.}'

rowct=0

# GET ALL URLS
f.next()

for row in f:
	urlstr=row[1]	
	urlstr=urlstr[urlstr.rfind('.com/')+len('.com/'):]
# 	print 'minus .com', urlstr
	for item in ['.jsp','?']:
		if urlstr.rfind(item)>-1:
			urlstr=urlstr[:urlstr.rfind(item)]
# 			print 'minus .com', item, urlstr
	if pageorder.count(urlstr)==0:
		pageorder.append(urlstr)
# 	else:
# 		print 'rejectedurlstr', urlstr
		
for item in pageorder:
	print 'cleanurl', item

# make object template:

mtrx['data']={}

csvfile.close()

csvfile=open('/Users/mgoold/Documents/NLTKProject/hotel6.14--6.28.13.txt','rU')

f = csv.reader(csvfile, delimiter='\t', quotechar="'")
f.next()

for row in f:	
	urlstr=row[1]	
	urlstr=urlstr[urlstr.rfind('.com/')+len('.com/'):]
# 	print 'minus .com', urlstr
	for item in ['.jsp','?']:
		if urlstr.rfind(item)>-1:
			urlstr=urlstr[:urlstr.rfind(item)]
		
	str=nltk.sent_tokenize(row[2])
	for sent in str: 
		if len(sent)>0:

			toks=sent.split()
			toks=[tok.lower() for tok in toks]
				
			for i in range(0,len(toks)):
				for sym in puncts:
					toks[i]=toks[i].replace(sym,'')				
					toks[i]=toks[i].strip()
			
			portstems=[]
							
			for tok in toks:
				if tok.rfind('booking')>-1:		
# 					print 'word is booking', tok	
					print 'lemmatized booking', lmtzr.lemmatize(tok,'v')		
					portstems.append(lmtzr.lemmatize(tok,'v'))
				else:
					portstems.append(lmtzr.lemmatize(tok))

# 			for word in stem_list:
			if 1==1:
# 				if portstems.count(word)>0:
				if 1==1:
				
					excerpt=[word.upper() for word in portstems if not word.lower() in stopwordslist]

					# excerpt=[word.upper() for word in portstems[portstems.index(word)+1:] if not word.lower() in stopwordslist]
					
					finder2=BigramCollocationFinder.from_words(excerpt)
					finder3=TrigramCollocationFinder.from_words(excerpt)
					scored2 = finder2.score_ngrams(bigram_measures.raw_freq)
					scored3 = finder3.score_ngrams(trigram_measures.raw_freq)
					sorted2=sorted(bigram for bigram, score in scored2)
					sorted3=sorted(trigram for trigram, score in scored3)
					
# 					print 'sorted2', sorted2
					
					for word in sorted2:
						word = ''.join(word)
						excerpt.append(word)
						
					for word in sorted3:
						word = ''.join(word)
						excerpt.append(word)

										
					for word in excerpt:
						if len(word)>0:						
							if word not in mtrx['data'].keys():
	# 							print 'not in data keys'
								ot={}
								for page in pageorder:
									ot[page]={}
									ot[page]['count']=0
									ot[page]['sent']=[]
								ot['total']=0
							
								mtrx['data'][word]=ot
							
								mtrx['data'][word]['total']=1
								mtrx['data'][word][urlstr]['count']=1
								templist=[]
								templist.append(sent)
								mtrx['data'][word][urlstr]['sent']=templist
							
							else:		
							
								mtrx['data'][word]['total']=mtrx['data'][word]['total']+1																				
								mtrx['data'][word][urlstr]['count']=mtrx['data'][word][urlstr]['count']+1	
																													
								templist=mtrx['data'][word][urlstr]['sent']
								templist.append(sent)
							
								mtrx['data'][word][urlstr]['sent']=templist		
						
# 						print 'word', word, 'url', urlstr, '''mtrx['data'][word]''', mtrx['data'][word]
														
# print 'mtrx[data]', mtrx
				
mtrx['data']=dict((k, v) for k, v in mtrx['data'].items() if v['total']>=40) 


# for x in mtrx['data'].keys() mtrx['data'][x]['total']>=2))
													
csvfile.close()

with open('/Users/mgoold/Documents/NLTKProject/hoteltopkwbyurl.json', 'wb') as fp:
    json.dump(mtrx, fp)

# sys.stdout = temp #restore print commands to interactive prompt
# sys.stdout.close() #ordinary file object



			
