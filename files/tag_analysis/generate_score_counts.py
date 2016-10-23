from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

score_counts = defaultdict(int)

with open("../all_gelbooru.xml", "r") as f:
# with open("../some_gelbooru.xml", "r") as f:
	for i, line in tqdm(enumerate(f), total=3004112):
		if i >= 0:
			# if i % 1000 == 0:
			# 	print("[{}] processing item {:07} / 3000000  unique scores: {}".format(timestamp(), i, len(score_counts)))
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				score = int(post["score"])
				score_counts[score] += 1


scores_file = open('res/scores.csv','w')
for w in tqdm(sorted(score_counts)):
# for w in tqdm(sorted(score_counts, key=score_counts.get, reverse=True)):
	scores_file.write("{:07},{}\n".format(w, score_counts[w]))
    # print w, score_counts[w]
scores_file.close()
