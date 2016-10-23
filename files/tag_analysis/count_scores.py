from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm


score_counts = [0]*2000

sample_size = 1E3
# sample_size = 10E3
# sample_size = int(1*100E3*2/3)
# sample_size = 3004112

with open("../all_gelbooru.xml", "r") as f:
	for i, line in tqdm(enumerate(f), total=sample_size):
		if i < sample_size:
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				score = int(post["score"])
				if score > 1000:
					print(post["id"])
				score_counts[score] += 1
		else:
			break


#write all the scores to a file
scores_file = open('res/score_counts.csv','w')

scores_file.write("score,count\n")
for score, count in tqdm(enumerate(score_counts)):
	scores_file.write("{},{}\n".format(score, count))

scores_file.close()


