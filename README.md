# Movies as a graph


## Abstarct
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
The idea is to represent the set of movies as a graph, where every movie is a vertex that is connected to all others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. It is expected that such a classification of movies divides them into clusters. This graph could then be used to suggest movies: "If you liked this movie, you might like \[top 5 connected vertices with highest edges\]". 

So, the motivation would be to create a movie recommender system, and for that we would like to present a way to find similar movies.




## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* If we create a graph with all the movies, is it possible to identify large clusters of movies interconnected with each other?
* With our approach, are we able to spot movies that are copies of some other movies? On the other hand are we able to spot movies that are similar to nothing?


## Data discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
We do not have an additional datasets because we can compute the similarities between movies with the datset we already have at our disposal.

There could be additional features that help us compute better the similarity, such as the director of the movie or the music or other characteristics.

Connecting all movies together might be too expensive computationally and might take to much space : with 42306 movies we would have 42'306×42'305÷2 = 894'877'665 edges. If each edge is a float (4 bytes), this would be equivalent to about 3.6 GB. To avoid having to store this much data we have considered a cutoff method, for example only keep edges above a certain value, or for each movie keep a limited number of bound movies.


## Methods

**Step 1:** Data scraping, pre-processing and dataset construction.

**Step 2:** Similarity function.

**Step 3:** Generate graph.

**Step 4:** Clustering ?

**Step 5:** Add visualization.

**Step 6:** Create movie recommender.

**Step 7:** Github site building and Datastory redaction.

Further details on the proposed data pipelines can be found in the notebook.


## Proposed timeline

* 01/12/2022 for step 1 
* 08/12/2022 for step 3
* 15/12/2022 for step 6
* 01/12/2022 for step 7 


## Organization within the team
[//]: # "A list of internal milestones up until project Milestone P3."

* Yucef: data scraping
* Camille: similarity function
* Taras: graph construction
* Léon: graph exploitation and visualization


## Questions for TAs
[//]: # "Add here any questions you have for us related to the proposed project."
