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
    integ_similiarity = np.zeros(distance_matrix.shape)
    idx_valid = np.where(~np.isnan(distance_matrix))
    idx_nan = np.where(np.isnan(distance_matrix))
    d_max = np.max(distance_matrix[idx_valid])
    d_min = np.min(distance_matrix[idx_valid])
    
    integ_similiarity[idx_valid] = (np.ones(distance_matrix[idx_valid].shape) - 
                              (distance_matrix[idx_valid]-d_min)/(d_max-d_min))  
    integ_similiarity[idx_nan] = 0
    
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
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
              " url_token ", doc)
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
        index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in corpus]], 
                                     similarity_matrix)
        headlines_similarity[i,:] = index[query_tf]
    return headlines_similarity


def similarity_fct(df):
    stopwords_headlines=['the','of','the','and','in','a','to','my','for','on','&','from']
    similarity_index = compute_similarity_index('glove-wiki-gigaword-50')
    jacc_genre = np.ones((df.shape[0], df.shape[0]))
    jacc_language = np.ones((df.shape[0], df.shape[0]))
    jacc_country = np.ones((df.shape[0], df.shape[0]))
    jacc_actors = np.ones((df.shape[0], df.shape[0]))
    jacc_characters = np.ones((df.shape[0], df.shape[0]))
    bin_director = np.ones((df.shape[0], df.shape[0]))
    bin_color = np.ones((df.shape[0], df.shape[0]))
    bin_runtime = np.ones((df.shape[0], df.shape[0]))
    integ_date = np.ones((df.shape[0], df.shape[0]))
    cosine_headlines = np.ones((df.shape[0], df.shape[0]))
    #soft_cosine_headlines = np.zeros((df.shape[0], df.shape[0]))
    ID_index = []

    matrices_dict = {}
    print('stockage_created')

    
    for i in range(len(df)):
        ID_index.append(df['name'][i])
        for j in range(len(df)):
            #fill only the half of the similarity matrices
            if(i<j):
                jacc_genre[i,j] = jaccard_similarity(df['genres'].iloc[i],df['genres'].iloc[j])
                jacc_language[i,j] = jaccard_similarity(df['languages'].iloc[i],df['languages'].iloc[j])
                jacc_country[i,j] = jaccard_similarity(df['countries'].iloc[i],df['countries'].iloc[j])
                jacc_actors[i,j] = jaccard_similarity(df['actors'].iloc[i],df['actors'].iloc[j])
                jacc_characters[i,j] = jaccard_similarity(df['characters'].iloc[i],df['characters'].iloc[j])
                bin_director[i,j] = binary_similarity(df['director'].iloc[i],df['director'].iloc[j])
                bin_color[i,j]= binary_similarity(df['color'].iloc[i],df['color'].iloc[j])
                bin_runtime[i,j]= binary_similarity(df['runtime'].iloc[i],df['runtime'].iloc[j])

                if( np.isnan(df['release_date'].iloc[i]) | np.isnan(df['release_date'].iloc[j]) ):
                    integ_date[i,j] = None
                else:
                    integ_date[i,j]=abs(df['release_date'].iloc[i]-df['release_date'].iloc[j])

    jacc_genre = jacc_genre+jacc_genre.transpose()
    np.fill_diagonal(jacc_genre, 1)

    jacc_language = jacc_language+jacc_language.transpose()
    np.fill_diagonal(jacc_language, 1)

    jacc_country = jacc_country+jacc_country.transpose()
    np.fill_diagonal(jacc_country, 1)  

    jacc_actors += jacc_actors.transpose()
    np.fill_diagonal(jacc_actors, 1)

    jacc_characters += jacc_characters.transpose()
    np.fill_diagonal(jacc_characters, 1)

    bin_director += bin_director.transpose()
    np.fill_diagonal(bin_director, 1)

    bin_color += bin_color.transpose()
    np.fill_diagonal(bin_color, 1)

    bin_runtime += bin_runtime.transpose()
    np.fill_diagonal(bin_runtime, 1)
    
    integ_date = integ_date+ integ_date.transpose()
    integ_date = integer_similarity(integ_date)    
    np.fill_diagonal(integ_date, 1)

    cosine_headlines = headlines_similarity(df['name'], stopwords_headlines)
    soft_cosine_headlines = headlines_soft_similarity(df['name'], stopwords_headlines, similarity_index)

    matrices_dict['genre'] = jacc_genre
    matrices_dict['language'] = jacc_language
    matrices_dict['countries'] = jacc_country
    matrices_dict['date'] = integ_date
    matrices_dict['actors'] = jacc_actors
    matrices_dict['characters'] = jacc_characters
    matrices_dict['director'] = bin_director
    matrices_dict['color'] = bin_color
    matrices_dict['runtime'] = bin_runtime
    matrices_dict['headlines'] = cosine_headlines
    matrices_dict['headlines_soft'] = soft_cosine_headlines

    return matrices_dict, ID_index





