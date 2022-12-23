# Movies as a graph


## Abstract
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
In this project we try to build a graph of movies. The idea is to represent each movie as a node, which is connected to others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. The motivation to build such a graph is to be able to study clusters of movies, and to try to study correlations between different features (for example, is the "Drama" genre more present in the american movies than in other cultures?). To compute this similarity we want to try a hand-crafted approach, where we compute the similarities of each feature we have (genre, plot, actors, characters, etc), and take a weighted sum of these similarities.

## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* If we create a graph with our method, will it be possible to identify large clusters of movies interconnected with each other or will the similarities "cancel out"?
* Assuming they split into clusters, what characterizes the different clusters?
* Is it possible to use the plots of movies to measure when movies are similar? (to be checked on sequels)
* How does a content-based recommendation algorithm (like the one we are building) compares to a user-based one ("users who have liked this movie have also liked [...]") ? What are the biases with one or the other method?


## Data size discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
To be able to tune the weights, we store the similarity matrix for each feature. While storage expensive (about 2.8 GB per feature), it gives us more flexibility to modify the graph. To store these matrices, we convert the similarity from the range 0-1 to the range 0-65'535 and store them in the format uint16. This is equivalent to working with fixed point numbers, where the LSB is 1/65'535.


### Additional dataset
In order to increase the number of useful attributes to calculate the similarity between films, a database made from scraping on wikidata is built. By starting with the Freebase ID, we collect the director and color (black and white vs color) features of the movies. We believe the director feature can help us to have more meaningful similarities, and the color, even though quite correlated to the release date, gives us additional information when in the transition period (in the 1950s). 

The code for the scraping is in a separated notebook, as we only need to run it once to collect the additional dataset.

## Methods

**Step 1: Exploratory data analysis, feature description, pre-processing, scraping, and dataset construction** 

* Manipulation of the data in order to explore it, and describe its most apparent features.
* Cleaning of the movie dataset and selection of the attributes can potentially help us in our similarity problem, without being too conservative. This allows us to tune the effect of each parameter online later. Search for correlated variables, or possible meaningful attributes associations. 
* Scraping in order to enrich the dataset with more descriptive attributes. 
* Formatting the data for step 2. 

**Step 2: Similarity between movies computation based on movie features** 
<ol>
  <li>Definition of the total similarity function between two movies. The total similarity is a weighted sum of the individual similarities based on each feature of the movie 
</li>
  <li>Computation of the similarity between movies for each feature. In all the following steps, when a movie attribute is not provided (NaN value), the resulting similarity with other movies is 0. For some features we propose several methods for similarity computing, the best method will be chosen in Milestone3 after comparing performances:
  <ul>
  <li>Word Categorical features: Movie genres, Movie Languages, Movie Countries, Actors, Characters. We use the jaccard similarity</li>
  <li>Binary features: Color (Movie in Colors - Movie in black and white), Runtime (long film - short film) and Director. We compute a binary similarity described in the notebook methods.</li>
  <li>Release year. We compute the Manhattan distance between the movie years, apply a Min-Max normalization and compute the associated similarity.
</li>
  <li>Movie title. We compute the cosine similarity on TF-IDF vectors associated to each movie title.
</li>
</ul></li>
  <li>Plot topic extraction. We use BERTopic to compute the different topics of our movies, and the probability of each topic for each movie. This gives us a vector for each movie, and we compare these vectors using a cosine similarity.
</li>
</ol>

**Step 3: Graph generation based on the similarity metric and graph visualization**
<ol>
  <li> We compute the similarity matrix for each feature. To validate if they are good, we can run it on sequels and see the values they give for each similarity.
</li>
  <li> Once this is done, we compute the total similarity function using all the similarity matrices.
</li>
  <li> We build the graph using the total similarity matrix. To do it, we add all the edges above a certain thershold. By adjusting the threshold we can adjust the number of edges in our graph. We tried to choose a threshold to minimize the numbers of edges but still try to connect all the movies between them, but we didn't manage to do so: the number of edges explodes within some clusters of movies while a lot of movies (about the half) are isolated. To avoid this, we limit the number of edges by movie to 30, and add the edges in descending order of their weights, to have the strongest one attached. With this we are able to choose a threshold to connect most movies together. Finally, to avoid having isolates, we connect the remaining nodes to theis closest movie.
</li>
  <li>We use the graph visualization tool Gephi specialized in representing graphs, and analyze it.
</li>
</ol>

**Step 4: Analysis of the similarity graph**

We split our movies into clusters using the Louvain method. We then analyze what are the characteristics of the big communities: what are the relevant genres, topics, actors, characters etc.


**Step 5: Github site-building and Datastory redaction**

Finally we build a site summarizing the datastory and the different visualizations we have built.

Further details on the proposed data pipelines can be found in the notebook.


## Proposed timeline
Deadlines correspondings to each step of the method.
* 18/11/2022: step 1
* 09/12/2022: steps 2 and 3
* 16/12/2022: steps 4 and 5
* 23/12/2022: step 6


## Organization within the team
[//]: # "A list of internal milestones up until project Milestone P3."

* Yucef: Data scraping, preprocessing and plots similarity
* Camille: Similarity of all features except plots, graph clustering
* Taras: Graph construction and visualization
* Léon: Github site-building, feature analysis
