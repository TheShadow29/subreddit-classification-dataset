# subreddit-classification-dataset
Create a subreddit classifier and have extensive study

There will be a few different tracks:
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
	- Also change the labels (or remove from the training set) by looking at the comments. Some comments may suggest that this is more appropriate to post on a different sub-reddit.
	- If some posts have been cross-posted to another sub-reddit, include the other sub-reddit as well.
	- Remove some corner-cases like potatosalad and john cena.
	- The noisy one has none of these removed.

4. Adherence to rules:
	- Different sub-reddits have different rules. Can have input as rules to be followed as a natural language and determine if a particular post is suitable for the particular sub-reddit or not.
	- Also based on certain features like day of the week, different sub-reddits have slightly different rules. Can take into consideration this, and create a more robust dataset which can even classify this field. (Slightly more complicated issue).

### Motivation:
1. If some user tries to post something, the model can do the following:
	- Suggest other sub-reddits they may enjoy.
	- Suggest if the content is appropriate for the particular subreddit.
	- Suggest if the user is abiding to all the rules of posting into the particular sub-reddit.
	- Give pointers to wheather the title/post should be altered (not suggesting a new one, only giving a score for the particular title).

### Important links:
1. A list of all sub-reddits: https://www.kaggle.com/rayraegah/subreddits
	- Will select a small subset for the coarse track small

2. Reddit API:
	- Full documentation: https://www.reddit.com/dev/api/
	- Full documentation on github wiki: https://github.com/reddit-archive/reddit/wiki/API
	- Simple tutorial with Python: https://www.pythonforbeginners.com/python-on-the-web/how-to-use-reddit-api-in-python/
	- Python Reddit API Wrapper: https://github.com/praw-dev/praw, https://praw.readthedocs.io/en/latest/

### ToDo:
- [ ] Create a small curated list of sub-reddits to use for coarse, fine-grained.
- [ ] Create a small sample dataset. Start with coarse. Then FineGrained. Titles/Posts segregated.
- [ ] Fileter out small cases.
- [ ] Propose good baseline models. AWD-LSTM pre-trained on wiki text should be a good start point.
- [ ] Test baseline models on larger dataset.

### Not To Do but good possible extensions:
1. Extend this to visual case. Popular examples would be meme sub-reddits. For example, seeing the meme, can the model decide if it should go to prequelmemes or sequelmemes or perhaps even trebuchetmemes.
2. Combine visual and nlp to get some kind of multi-modal reasoning.

### How to Use:
1. Download the subreddit list in the csv format inside a folder called data.
2. Install the dependencies via `pip install -r requirements`. Suggested to use a python 3.6 environment.
3. Create a `praw.ini` file in the `src` directory. Check https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html for more information on how to set up the `.ini` file. Name the bot as `scraper`.
