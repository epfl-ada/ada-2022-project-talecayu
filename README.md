# Movies as a graph


## Abstract
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
The idea is to represent the set of movies as a graph, where every movie is a vertex that is connected to all others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. It is expected that such a classification of movies divides them into clusters. This graph could then be used to suggest movies: "If you liked this movie, you might like \[top 5 connected vertices with highest edges\]". Building such a graph will allow us to explore how the movies are interconnected to each other and what is the best predictor to find similar movies. The movie recommendation system that we will create will give us insight on how such algorithm work, will make us define what makes two movies similar and will emphasise the bias of this choice on the recommendation.

## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* If we create a graph with all the movies, is it possible to identify large clusters of movies interconnected with each other?
* (Assuming they split into clusters) what are the characteristics of the biggest cluster?
* With our approach, are we able to spot movies that are influenced by other movies? On the other hand are we able to spot movies that are similar to no others?
* How does a content-based recommendation algorithm (like the one we are building) compares to a user-based one ("users who have liked this movie have also liked [...]") ? What are the biases with one or the other method?


## Data size discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
Connecting all movies together (with an adjacency matrix) might be too expensive in storage : with 42306 movies we would have 42'306×42'305÷2 = 894'877'665 edges. If each edge is a float (4 bytes), this would be equivalent to about 3.6 GB. So instead we will build the graph as an adjacency list, and store only the closest 100 movies. We keep more than the number of movies we'll recommend to be able to apply filters to the output (by language for example) without having to recompute the whole graph.

### Additional dataset
In order to increase the number of useful attributes to calculate the similarity between films, a database made from scraping on wikidata is built. By starting with the ‘Freebase ID’, one collects additional information such as the movie director, the color of the movie, the location of the movie, the composer, etc. 
The director and color attributes being the least sparse, we decided to add them to the cleaned movie metadata. 

Observe the corresponding scrapping section in the notebook for libraries and code specifications. 

## Methods

**Step 1: Exploratory data analysis, feature description, pre-processing, scraping, and dataset construction** 
* Manipulation of the data in order to explore it, and describe its most apparent features.
* Cleaning of the movie dataset and selection of the attributes that can potentially help us in our similarity problem, without being too conservative. This allows us to tune the effect of each parameter online later. Search for correlated variables, or possible meaningful attributes associations. 
* Scraping in order to enrich the dataset with more descriptive attributes. 
* Formatting the data for step 2. 

**Step 2: Similarity between movies computation based on movie features** 
<ol>
  <li>Definition of the total similarity function between two movies. The total similarity is a weighted sum of the individual similarities based on each feature of the movie 
</li>
  <li>Computation of the similarity between movie for each feature. In all the following steps, when a movie attribute is not provided (NaN value), the resulting similarity with other movies is 0. For some features we propose several methods for similarity computing, the best method will be chosen in Milestone3 after comparing performances:
  <ul>
  <li>Word Categorical features: Movie genres, Movie Languages, Movie Countries, Actors, Characters, Director. We use the jaccard similarity</li>
  <li>Binary features: Color (Movie in Colors - Movie in black and white), Runtime (long film - short film). We compute a binary similarity described in the notebook methods.</li>
  <li>Release year. We compute the Manhattan distance between the movie years, apply a Min-Max normalization and compute the associated similarity.
</li>
  <li>Movie title. We try 2 different methods: computation of the cosine similarity on TF-IDF vectors associated to each movie title and computation of the soft cosine similarity based on a similarity matrix computed with the GloVe algorithm and associated model: glove-wiki-gigaword-50.model 
</li>
</ul></li>
  <li>Plot topic extraction. Using Doc2Vec, LDA or BERTopic we compute a vector representing the topics present in the plot (the Doc2Vec is trained directly to give a vector, for the other two we build it from the frequency/probability of each topic). To compare plots between movies we compute the cosine similarity of their representing vectors.
</li>
</ol>

**Step 3: Graph generation based on the similarity metric and graph visualisation**

<ol>
  <li>Once the similarity function is built, and we have a global metric, we can test if it works well on a subset of movies. We compute the similarity in all possible pairs of movies in the subset and store the result to build a small version of the graph. We can also tune the weights of each feature and see the changes it implies in the graph.
</li>
  <li>To validate if our global metric is good, we can run it on sequels which we expect to have a high similarity. We can also run it on movies that we expect to have very little in common, for example movies with completely different genres, and check if the similarity is close to 0.
</li>
  <li>Once the global metric is validated, for each movie we compare it to all other movies, sort them by similarity, and store the closest 100. Thus for each movie we will have a list of the top 100 closest movies, creating an adjacency list. This will be our weighted directed graph representation.
</li>
  <li>We use a graph visualization tool like Gephi specialized in representing graphs, and analyze it.
</li>
</ol>

**Step 4: Analysis of the similarity graph**

Since we expect the movies to split into clusters, we will run some graph clustering algorithms (like “Edge Betweenness clustering” or “Biconnected components clustering”) and see if the generated clusters are meaningful.

**Step 5: User recommendation algorithm** 

The user gives a movie, and using the graph adjacency list directly we suggest the top 5 or 10 most similar movies. We will also add the option to use filters, to remove movies with certain languages or from certain release date/countries.

**Step 6: Github site building and Datastory redaction**

Finally we build a site summarizing the datastory and the different visualizations we have built, including the user recommendation algorithm.

Further details on the proposed data pipelines can be found in the notebook.


## Proposed timeline
Deadlines correspondings to each step of the method.
* 18/11/2022: step 1
* 09/12/2022: steps 2 and 3
* 16/12/2022: setps 4 and 5
* 23/12/2022: step 6


## Organization within the team
[//]: # "A list of internal milestones up until project Milestone P3."

* Yucef: Data scraping and preprocessing
* Camille: Similarity of all features except plots
* Taras: Similarity of plots, graph construction 
* Léon: Graph exploitation and visualization
* All together: Github site building
