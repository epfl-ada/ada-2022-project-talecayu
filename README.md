# Movies as a graph


## Abstarct
[//]: # "Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?"
The idea is to represent the set of movies as a graph, where every movie is a vertex that is connected to all others through weighted edges. Similar movies (like sequels) will have high-valued edges interconnecting them. It is expected that such a classification of movies divides them into clusters. This graph could then be used to suggest movies: "If you liked this movie, you might like [top 5 connected vertices with highest edges]". After building such a graph, we can analyze the evolution of such a graph over time. 

So, the motivation would be to create a movie recommender system, and for that we would like to present a way to find similar movies.


## Research Questions
[//]: # "Research Questions: A list of research questions you would like to address during the project."
* Can movies be split into clusters?
* Is it possible to transform plot summaries into easily comparable data?

If movies can be split into clusters:

* When looked into in a chronological order, how often do movies appear that are different from what was present before?
* Did a new cluster appear in the recent years, or can all new movies be classified into the already existing ones?


## Data discussion
[//]: # "Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible."
In our case we don't need an additional dataset, we can use the already present features to compute similarity. Instinctively it should be possible using the plot summary, movie genre, titles and maybe actors and country of origin. Theoretically there could be additional features that help us compute better the similarity, like having the full plot instead of the summary, or having users feedback ("users who watched this movie also like this one"), but we're probably not going to look for them. To be able to compare plots efficiently we will need to convert them to "simpler" data, with less dimensions. This can be done by using a list of keywords or an embedding. For this an algorithm (possibly a trained Machine Learning algorithm) could be used.

Connecting all movies together might be too expensive computationally and might take to much space : with 42306 movies we would have 42'306×42'305÷2 = 894'877'665 edges. If each edge is a float (4 bytes), this would be equivalent to about 3.6 GB. To avoid having to store this much data we should consider a cutoff method, for example only keep edges above a certain value, or for each movie only store a certain ammount of closest movies.


## Methods


## Proposed timeline


## Organization within the team
[//]: # "A list of internal milestones up until project Milestone P3."


## Questions for TAs
[//]: # "Add here any questions you have for us related to the proposed project."
