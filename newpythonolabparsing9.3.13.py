
import nltk
import csv
from nltk.corpus import stopwords
from urlparse import urlparse
from nltk.collocations import *
from nltk.stem.wordnet import WordNetLemmatizer
import sys
from operator import itemgetter
import json
import HTMLParser
import pyolab_help as ph
from sys import argv 

print 'argv', argv

script, stem_list, test_title, min, start_date, end_date,subdomain,notsubdomain= argv

print 'script',script
print 'stem_list', stem_list
print 'test_title', test_title
print 'min', min, 'type', type(min)


stem_list=stem_list.split(' ')

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
# sys.stdout = open('/Users/user/Documents/NLTKProject/log.txt','w') #redirect all prints to this log file

nWords=10
puncts='1234557890#{}[].?!,\'\"'

# porter = nltk.PorterStemmer()
lmtzr = WordNetLemmatizer()

# DESIRE=first
# DESIRE=DESIRE
# DESIRE=['error','problem','suck','issue','broken','wont','dont','cant','hate']
pageorder=[]
# pageorder=['hotels/results-opaque','hotels/results','hotels/searchResults','hotels/searchResults/sort']
outputlist={}

desire_list=''

for item in stem_list:
	desire_list=desire_list+','+item

# GET TITLE
# test_title=second

# setup matrix
mtrx=autoviv() #special class for automatically nesting dictionaries
mtrx['d3layout']='stack'
mtrx['chartsub']='bar'
mtrx['release']='13.08'
mtrx['startdate']='01-APR-2013'
mtrx['enddate']='30-APR-2013'
mtrx['charttitle']=test_title
mtrx['chartnote']='{Keyword counts for comments having words:'+ desire_list+'.}'


# HANDLE STOP WORDS
stopwordadditions=['site','hotel','room','review','would','hotwire','hotels','flight','car','rent']
stopwordadditions=stopwordadditions+stem_list

stopwordslist=stopwords.words('english')

for i in range(0,len(stopwordadditions)):
	stopwordslist.append(stopwordadditions[i])

rowct=0

# GET ALL URLS
# f.next()

root=ph.get_olab_root('user@domain.com','password',start_date,end_date,'domain','www.yourdomain.com')

mtrx['data']={}

# subdomain='hotel'
# notsubdomain='mobile'

if type(root)=='NoneType':
	print 'nonetype found'

for element in root.findall('.//data'):
	urlstr = element.findall('url')[0].text	
	urlstr=urlstr[urlstr.rfind('.com/')+len('.com/'):]
# 	print 'minus .com', urlstr
	for item in ['.jsp','?','%','LXeTUmCW']:
		if urlstr.rfind(item)>-1:
			urlstr=urlstr[:urlstr.find(item)]
# 			print 'minus .com', item, urlstr
	if pageorder.count(urlstr)==0 and urlstr.rfind(subdomain)>-1 and urlstr.rfind(notsubdomain)==-1:
		pageorder.append(urlstr)
# 	else:
# 		print 'rejectedurlstr', urlstr

for item in pageorder:
	print 'cleanurl', item

# make object template:

# 
# csvfile.close()
# 
# csvfile=open('/Users/mgoold/Documents/NLTKProject/hotel07_03-2013_07_16.txt','rU')
# 
# f = csv.reader(csvfile, delimiter='\t', quotechar="'")
# f.next()

# for row in f:	

for element in root.findall('.//data'):
	urlstr = element.findall('url')[0].text	
	urlstr=urlstr[urlstr.rfind('.com/')+len('.com/'):]
# 	print 'minus .com', urlstr
	for item in ['.jsp','?','%','LXeTUmCW']:
		if urlstr.rfind(item)>-1:
			urlstr=urlstr[:urlstr.find(item)]
# 			print 'minus .com', item, urlstr
		
	if urlstr in pageorder:
		str = element.findall('comments')[0].text
		str=nltk.sent_tokenize(str)
		for sent in str:
			sent=sent.encode("utf_8","replace")
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
	# 					print 'lemmatized booking', lmtzr.lemmatize(tok,'v')		
						portstems.append(lmtzr.lemmatize(tok,'v'))
					else:
						portstems.append(lmtzr.lemmatize(tok))

				
				for word in stem_list:
					if portstems.count(word)>0:
				
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
				
mtrx['data']=dict((k, v) for k, v in mtrx['data'].items() if v['total']>=int(min))
													
with open('/Users/mgoold/Documents/D3Project/topkwbyurl.json', 'wb') as fp:
    json.dump(mtrx, fp)

fp.close()

# sys.stdout = temp #restore print commands to interactive prompt
# sys.stdout.close() #ordinary file object
















			