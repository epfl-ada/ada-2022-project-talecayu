import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import seaborn as sns

from re import sub

import gensim
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity
from gensim.models.word2vec import Word2Vec


def dot(A,B): 
  return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity_simple(a,b):
  """ returns cosine similarity between two lists """
  return dot(a,b)/((dot(a,a)**.5)*(dot(b,b)**.5)) 

def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two sets x and y"""
  intersection_cardinality = len(set.intersection(*[x, y]))
  union_cardinality = len(set.union(*[x,y]))
  if union_cardinality == 0:
    return 0.0
  else:
    return intersection_cardinality/float(union_cardinality)

def isNaN(string):
    return string != string

def binary_similarity(x,y):
    '''
    returns the similarity in values of 
    0 or 1
    '''
    if(isNaN(x) | isNaN(y)):
        return 0
    if(x==y):
        return 1
    else:
        return 0   

def integer_similarity(distance_matrix):
    '''
    inputs: matrice of distances
    output: similarity associated to normalized manhattan distance
    '''

    integ_similiarity=np.zeros(distance_matrix.shape)
    
    idx=np.where(~np.isnan(distance_matrix))
    idx2=np.where(np.isnan(distance_matrix))

    d_max = np.max(distance_matrix[idx])
    d_min = np.min(distance_matrix[idx])
    
    integ_similiarity[idx]=np.ones(distance_matrix[idx].shape) - (distance_matrix[idx]-d_min)/(d_max-d_min)    
    integ_similiarity[idx2]=0
    
    return integ_similiarity

def headlines_similarity(df_headlines, list_stopwords):
    documents = list(df_headlines)
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(lowercase=True,stop_words=list_stopwords)
    X = vectorizer.fit_transform(documents)
    list_vectors = X.toarray()
    headlines_similarity=sklearn.metrics.pairwise.cosine_similarity(list_vectors)
    
    return headlines_similarity

def preprocess(doc, stopwords):
    # From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
    # Tokenize, clean up input document string
    doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    doc = sub(r'<[^<>]+(>|$)', " ", doc)
    doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

def compute_similarity_index(model_name):
    # From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
    model = api.load(model_name)     
    similarity_index = WordEmbeddingSimilarityIndex(model)
    return similarity_index

def headlines_soft_similarity(df_headlines, stopwords, similarity_index):
    # From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
    documents = list(df_headlines)
    headlines_similarity=np.zeros([len(documents),len(documents)])

    # Preprocess the documents
    corpus = [preprocess(document,stopwords) for document in documents]
    dictionary = Dictionary(corpus)
    tfidf = TfidfModel(dictionary=dictionary)
    # Create the term similarity matrix.  
    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

    for i in range(len(documents)):
        query_tf = tfidf[dictionary.doc2bow(corpus[i])]
        index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in corpus]],similarity_matrix)
        headlines_similarity[i,:] = index[query_tf]

    return headlines_similarity





