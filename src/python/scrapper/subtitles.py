import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import zipfile
import io
from os import listdir
from os.path import isfile, join

def extractLines(content):
	regex = r"(\d+)\r\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\r\n((.*\n)*?)\r\n"
	compiledRegex = re.compile(regex)
	return [(match.group(1), match.group(2), match.group(3), match.group(4)) for match in re.finditer(compiledRegex, content)]

def extractZipFiles(path):
	with zipfile.ZipFile(path) as zipFile:
		filePaths = zipFile.namelist()
		zipDF = pd.DataFrame(filePaths, columns=["filename"])

		def findSeasonAndEpisode(filename):
			match = re.search("(\d{1,2}).(\d{1,2})", filename)
			content = zipFile.open(filename).read().decode('UTF-8', errors='ignore')
			#print(extractLines(content))
			return int(match.group(1)), int(match.group(2))

		zipDF[["season","episode"]]= pd.DataFrame(zipDF["filename"].map(findSeasonAndEpisode).tolist(), columns = ["season","episode"])

		oneEpisodeDF = zipDF.groupby(["season", "episode"]).agg({"filename":"max"}).reset_index()
		oneEpisodeDF["lines"] = oneEpisodeDF["filename"].map(lambda fn: list(extractLines(zipFile.open(fn).read().decode('UTF-8', errors='ignore'))))

		#print(oneEpisodeDF)
		rows = []
		oneEpisodeDF.apply(lambda row : [rows.append([row["season"], row["episode"], lineNumber, startTime, endTime, lines]) for (lineNumber, startTime, endTime, lines) in row.lines], axis=1)

		cleanDF = pd.DataFrame(rows, columns = ["season", "episode", "line_number", "start_time", "end_time", "lines"])

		return cleanDF

		
		
subtitleDir = "../../../data/subs"

zipFiles = [join(subtitleDir, f) for f in listdir(subtitleDir) if isfile(join(subtitleDir, f))]

completeDF = extractZipFiles(zipFiles[0])
for zipFile in zipFiles[1:]:
	completeDF = completeDF.append(extractZipFiles(zipFile))

completeDF.to_csv("../../../data/episode_subs.csv", index=False)

