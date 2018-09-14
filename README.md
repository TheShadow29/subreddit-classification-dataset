# subreddit-classification-dataset
Create a subreddit classifier and have extensive study

There will be two main tracks:
1. Coarse track: Based on only the title
    - small
    - big
2. Fine grained track:
    - Based on only the title
    - Based on both title and the post content.
3. Noisy and Clean Data:
    - Cleaning will require some form of pre-processing. 
    - Preprocessing could include removing posts with less than a certain number of upvotes.
    - Could also remove controversial posts.
    - Also change the labels via looking at the comments. Some comments may suggest that this is more appropriate to post on a different sub-reddit.
    - Also based on certain features like day of the week, different sub-reddits have slightly different rules. Can take into consideration this, and create a more robust dataset which can even classify this field. (Slightly more complicated issue).
### Important links:
1. A list of all sub-reddits: https://www.kaggle.com/rayraegah/subreddits
    - Will select a small subset for the coarse track small
    
2. Reddit API:
    - Full documentation: https://www.reddit.com/dev/api/
    - Full documentation on github wiki: https://github.com/reddit-archive/reddit/wiki/API
    - Simple tutorial with Python: https://www.pythonforbeginners.com/python-on-the-web/how-to-use-reddit-api-in-python/
    - Python Reddit API Wrapper: https://github.com/praw-dev/praw, https://praw.readthedocs.io/en/latest/
    
### ToDo:
- [ ] Create a small curated list of sub-reddits to use.
- [ ] Create a small sample dataset. Start with coarse. Then FineGrained. Titles/Posts segregated.
- [ ] Fileter out small cases. 
- [ ] Propose good baseline models. AWD-LSTM pre-trained on wiki text should be a good start point.
- [ ] Test baseline models on larger dataset. 

### Not To Do but good possible extensions:
1. Extend this to visual case. Popular examples would be meme sub-reddits. For example, seeing the meme, can the model decide if it should go to prequelmemes or sequelmemes or perhaps even trebuchetmemes. 
2. Combine visual and nlp to get some kind of multi-modal reasoning. 
