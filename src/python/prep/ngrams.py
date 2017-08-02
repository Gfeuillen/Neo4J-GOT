import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk.data
import string

stopWords = stopwords.words("english")

subsDF  = pd.DataFrame.from_csv("../../../data/episode_subs.csv", index_col=None)
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')


lines = subsDF["lines"]

# Break in sentences
sentences = lines.dropna()\
	.apply(lambda fullText: sent_detector.tokenize(fullText)) \
	.apply(pd.Series) \
	.unstack() \
	.reset_index(drop=True)


punctDict = dict.fromkeys(map(ord, string.punctuation))
for k in punctDict:
	punctDict[k] = " "

# Break sentences into words
words = sentences.dropna().apply(
	lambda sentence: word_tokenize(
		sentence
		.lower()
		.replace("\n","")
		.translate(punctDict)
		)
	)

# Filter stop words
filteredWords = words.apply(lambda words: [word for word in words if word not in stopWords])

# Desired grams
n_ngrams = 2

# Apply ngrams and flatten
ngrams = filteredWords \
	.apply(lambda words: [[words[i], words[i+1]] for i in range(len(words)-n_ngrams)]) \
	.apply(pd.Series) \
	.unstack() \
	.reset_index(drop=True)


# Put all of that in DF
ngramsDF = pd.DataFrame(ngrams.dropna().tolist(), columns = ["gram_{:d}".format(i) for i in range(n_ngrams)])

# Save it
ngramsDF.to_csv("../../../data/ngrams.csv", index=False)
