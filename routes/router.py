from flask import jsonify
import math
import nltk # NLP library
from nltk.corpus import stopwords # Get list of stop words

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

"""Calculates Tf-Idf score
@type tf: int
@param tf: raw term count
@type totalWords: int
@param totalWords: word count
@type totalDocs: int
@param totalDocs: total document count
@type docsContaining: int
@param docsContaining: count of docs containing specified word
@rtype: float
@returns: tf-idf score
"""
def tfIdf(tf, totalWords, totalDocs, docsContaining):
        #term Frquency - count/totalWords
        tf = tf / totalWords # normalize term frequency with totalWords
        idf = math.log(totalDocs / docsContaining) # Log idf to give high frequency words lower scores
        score = tf * idf
        return score * 1000 # Multiply by 1000 for whole number comparison


"""Extract Important words Tf-Idf score
@type files: list
@param files: list of documents
@rtype: list
@returns: list of objects containing word data, sorted by score
"""
def extractWords(files):
    numOfDocs = len(files)

    if (numOfDocs <= 1):
        raise Exception('Number of documents must be greater than 1')

    tokenizer = nltk.RegexpTokenizer(r"\w+") # Tokenizer to remove punctuation
    count = dict() # Count dictory to track word information
    important = [] # List to return important words
    totalWords = 0 # Initialize total words amongst all docs

    # Iterate through documents
    for doc in files:
        text = files[doc].read().decode()
        totalWords += len(tokenizer.tokenize(text))
        sentences = nltk.sent_tokenize(text) # split into sentences
        for sentence in sentences:
            words = tokenizer.tokenize(sentence) # split sentences into individual words
            for word in words:

                ''' 
                If the word has been seen, increment count, 
                add the sentence to the sentences if it has not been added already, 
                add the document name to the doc list if it has not been added,
                and update score.

                If the word has not been seen,
                add it to count,
                calculate initial score,
                and add approrpiate doc, sentence and score
                '''
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
    #After word tfidf scores have been found, add most important words to a list and sort from highest to lowest score
    important = []
    for k, v in count.items():
        if k not in stop_words:
            important.append(
                {'word': k, 
                'docs': count[k]['docs'], 
                'sentences':count[k]['sentences'],
                'score': count[k]['score']
                })
    top_one_percent = math.floor(len(important)/100)
    important.sort(key=lambda json: json['score'], reverse=True)
    return important[:top_one_percent]
