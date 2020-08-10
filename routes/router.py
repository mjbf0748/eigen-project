from flask import jsonify
import math
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def tfIdf(tf, totalWords, totalDocs, docsContaining):
        #term Frquency - count/totalWords
        tf = tf / totalWords
        idf = math.log(totalDocs / docsContaining)
        score = tf * idf
        return score * 1000



def extractWords(files):
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    count = dict()
    numOfDocs = len(files)
    important = []
    totalWords = 0

    for doc in files:
        text = files[doc].read().decode()
        totalWords += len(tokenizer.tokenize(text))
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            words = tokenizer.tokenize(sentence)
            for word in words:
                if word in count:
                    count[word]['tf'] += 1
                    if sentence not in count[word]['sentences']:
                        count[word]['sentences'].append(sentence)
                    if doc not in count[word]['docs']:
                        count[word]['docs'].append(doc)

                    score = tfIdf(count[word]['tf'], totalWords, numOfDocs, len(count[word]['docs']))
                    count[word]['score'] = score
                else:
                    initialDocScore = tfIdf(1, totalWords, numOfDocs, 1)

                    count[word] = {
                        'docs': [doc],
                        'tf': 1,
                        'sentences': [sentence],
                        'score': initialDocScore
                    }
    important = []
    for k, v in count.items():
        score = v['score']
        if score > 1 and k not in stop_words:
            important.append(
                {'word': k, 
                'docs': count[k]['docs'], 
                'sentences':count[k]['sentences']})
    
    return important

    

    



    