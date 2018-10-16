### Tracking Progress
1. Created a new csv file from the existing list of all subreddits to include fields like 'allow_images/videos/gifs', 'over18', 'public_description'. Also filter based on minimum subscriber count as 2000. 
2. Choose only the text based ones (which don't allow any images/videos/gifs). 
3. For each subreddit, segment the name of the subreddit.
4. Use spacy to get relevant word embeddings.
5. Get a similarity score using cosine similarity function of scikit-learn, take average of mean and max.
6. Make fully connected graph with subreddits as nodes. Edge contains the similarity between nodes.
7. Use community detection algorithms for clustering. However, results with lower similarity score thresholding not very impressive. Higher thresholds lead to many singletons. 
