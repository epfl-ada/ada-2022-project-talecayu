# Movies as a graph


## Abstarct
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
The idea is to represent the set of movies as a graph, where every movie is a vertex that is connected to all others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. It is expected that such a classification of movies divides them into clusters. This graph could then be used to suggest movies: "If you liked this movie, you might like \[top 5 connected vertices with highest edges\]". Building such a graph will allow to explore how the movies are interconnected to each other and what is the best predictor to find similar movies. The movie recommandation system that we will create will us give us insight in how such algorithm work, will make us define what makes two movies similar and will emphasise the bias of this choice on the recommandation.

## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* If we create a graph with all the movies, is it possible to identify large clusters of movies interconnected with each other?
* (Assuming they slit into clusters) what are the characteristics of the biggest cluster?
* With our approach, are we able to spot movies that are copies of some other movies? On the other hand are we able to spot movies that are similar to no others?
* How does a data-based recommandation algorithm (like the one we are building) compares to a user-based one ("users who have liked this movie have also liked [...]") ? What are the biases with one or the other method?


## Data discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
Connecting all movies together (with an adjacency matrix) might be too expensive in storage : with 42306 movies we would have 42'306×42'305÷2 = 894'877'665 edges. If each edge is a float (4 bytes), this would be equivalent to about 3.6 GB. So instead we will build the graph as an adjacency list, and store only the closest 100 movies. We keep more than the number of movies we'll recommand to be able to apply filters to the output (by language for example) without having to recompute the whole graph.

### Additional dataset
Additional datasets are not required, as we can already find a similarity function without them. However, we can find features that might give us features that help us to better predict movies similarities, like the director of a movie or knowing if the movie is in color or black and white. We can get this data by scraping through the wikipedia pages. 

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
