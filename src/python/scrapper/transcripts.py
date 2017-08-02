import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def makeRequest(url):
	headers = {
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
	}
	return requests.get(url,  stream=True, headers=headers)

def extractTranscript(transcriptURL):

	r = makeRequest(transcriptURL)
	soup = BeautifulSoup(r.text, 'html.parser')

	body = soup.find("div", attrs={"class":"postbody"})

	texts = [p.text for p in body.find_all("p")]

	return texts

def extractEpisodesTranscriptsURL(url):

	r = makeRequest(url)
	soup = BeautifulSoup(r.text, 'html.parser')

	body = soup.find("div", attrs={"class":"postbody"})
	lines = body.find_all("p")
	linesWithLink = [(line, line.find("a", href=True)) for line in lines]
	linesFiltered = [(line, link.extract()) for (line, link) in linesWithLink if link is not None ]
	linesWithText = [(line.text, link.text, link["href"]) for (line, link) in linesFiltered]
	episodeLinks = [(beforeText, linkText, link, re.match("(\d{1,2}).(\d{2})", beforeText)) for (beforeText, linkText, link) in linesWithText]
	clearLinks = [(int(match.group(1)), int(match.group(2)), linkText, link) for (beforeText, linkText, link, match) in episodeLinks if match]

	return clearLinks


clearLinks = extractEpisodesTranscriptsURL("http://transcripts.foreverdreaming.org/viewtopic.php?t=7739")
episodeAndLines = [(season, episode, name, extractTranscript(link)) for (season, episode, name, link) in clearLinks]

fullDF = pd.DataFrame(columns=["text", "episode", "season", "name"])
for (season, episode, name, texts) in episodeAndLines:
	episodeDF = pd.DataFrame(texts, columns=["text"])
	episodeDF["episode"] = episode
	episodeDF["season"] = season
	episodeDF["name"] = name

	fullDF = fullDF.append(episodeDF, ignore_index=True)

fullDF.to_csv("../../../data/episode_lines.csv", index=False)