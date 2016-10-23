from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

tag_counts = dict()

with open("../all_gelbooru.xml", "r") as f:
# with open("../some_gelbooru.xml", "r") as f:
	for i, line in enumerate(f):
		if i < 100E3:
			if i % 1000 == 0:
				print("[{}] processing item {:07} / 3000000  unique tags: {}".format(timestamp(), i, len(tag_counts)))
			# print(line)
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				tags = post["tags"].strip().split(" ")
				# print(tags)

				for tag in tags:
					if tag not in tag_counts:
						tag_counts[tag] = (0, 0, 0)

					(s, q, e) = tag_counts[tag]
					rating = post["rating"]
					if rating == 's':
						s += 1
					elif rating == 'q':
						q += 1
					elif rating == 'e':
						e += 1
					tag_counts[tag] = (s, q, e)


#calculate the ecchi-ness score for each tag (higher is H-er)
def get_ecchi_score(x):
	(s, q, e) = x

	# s = max(s, 1)
	# ecchi_score = 1.0*e/s

	ecchi_score = 1.0*(e-s)/(e+q+s)

	return ecchi_score

def is_well_counted(x):
	(s, q, e) = x
	return (e+s >= 100)

tags_and_escores = [(tag, get_ecchi_score(tag_counts[tag])) for tag in tag_counts if is_well_counted(tag_counts[tag])]
tags_and_escores = sorted(tags_and_escores, key=lambda x: x[1])

#write all the scores to a file
tags_file = open('res/rating_tag_counts.csv','w')

for tag, score in tqdm(tags_and_escores):
	# print("{} {}".format(int(score), tag))
	tags_file.write("{} {}\n".format(score, tag))

tags_file.close()

