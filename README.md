# Movies as a graph


## Abstarct
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
The idea is to represent the set of movies as a graph, where every movie is a vertex that is connected to all others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. It is expected that such a classification of movies divides them into clusters. This graph could then be used to suggest movies: "If you liked this movie, you might like \[top 5 connected vertices with highest edges\]". Building such a graph will allow to explore how the movies are interconnected to each other and what is the best predictor to find similar movies. The movie recommandation system that we will create will give us insight on how such algorithm work, will make us define what makes two movies similar and will emphasise the bias of this choice on the recommandation.

## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* If we create a graph with all the movies, is it possible to identify large clusters of movies interconnected with each other?
* (Assuming they split into clusters) what are the characteristics of the biggest cluster?
* With our approach, are we able to spot movies that are influenced by other movies? On the other hand are we able to spot movies that are similar to no others?
* How does a content-based recommandation algorithm (like the one we are building) compares to a user-based one ("users who have liked this movie have also liked [...]") ? What are the biases with one or the other method?


## Data size discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
Connecting all movies together (with an adjacency matrix) might be too expensive in storage : with 42306 movies we would have 42'306×42'305÷2 = 894'877'665 edges. If each edge is a float (4 bytes), this would be equivalent to about 3.6 GB. So instead we will build the graph as an adjacency list, and store only the closest 100 movies. We keep more than the number of movies we'll recommand to be able to apply filters to the output (by language for example) without having to recompute the whole graph.

### Additional dataset
xxx to be changed with scraping choice, methods and outputs, -> yucef
Additional datasets are not required, as we can already find a similarity function without them. However, we can find features that might give us features that help us to better predict movies similarities, like the director of a movie or knowing if the movie is in color or black and white. We can get this data by scraping through the wikipedia pages. 

## Methods

**Step 1: Exploratory data analysis, feature description, pre-processing, scraping, and dataset construction.** 
xxx explain

**Step 2: Similarity between movies computation based on movie features** 

**Step 3: Graph generation based on the similarity metric and graph visualisation**

**Step 4: Analysis of the similarity graph**

**Step 5: User recommandation algorithm** 

**Step 6: Github site building and Datastory redaction**

Further details on the proposed data pipelines can be found in the notebook.


## Proposed timeline
Deadlines correspondings to each step of the method.
* 18/11/2022: step 1
* 09/12/2022: steps 2 and 3
* 16/12/2022: setps 4 and 5
* 23/12/2022: step 6


## Organization within the team
[//]: # "A list of internal milestones up until project Milestone P3."

* Yucef: data scraping
* Camille: similarity function
* Taras: graph construction
* Léon: graph exploitation and visualization
