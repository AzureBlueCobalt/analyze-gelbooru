from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


# sample_size = 1E3
# sample_size = 10E3
# sample_size = 1*100E3
sample_size = -1


tag_counts = dict()

if sample_size == -1:
	sample_size = 3004112
with open("../all_gelbooru.xml", "r") as f:
	for i, line in tqdm(enumerate(f), total=sample_size):
		if i < sample_size:
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				tags = post["tags"].strip().split(" ")

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
		else:
			break

#calculate the ecchi-ness score for each tag
def get_ecchi_score(x):
	(s, q, e) = x

	# s = max(s, 1)
	# ecchi_score = 1.0*e/s #higher is H-er

	# ecchi_score = 1.0*(e-s)/(e+q+s)

	ecchi_score = e-s

	return ecchi_score

def is_well_counted(x):
	(s, q, e) = x
	
	if (e+s+q < 2000):
		return False

	e_score = 1.0*e/(e+q+s)
	q_score = 1.0*q/(e+q+s)
	s_score = 1.0*s/(e+q+s)

	threshold = 0.8

	return (abs(e_score) >= threshold) or (abs(q_score) >= threshold) or (abs(s_score) >= threshold)
	
	# return True

	# return (e+s >= 1000)

tags_and_escores = [(tag, get_ecchi_score(tag_counts[tag])) for tag in tag_counts if is_well_counted(tag_counts[tag])]
tags_and_escores = sorted(tags_and_escores, key=lambda x: x[1])

#write all the scores to a file
tags_file = open('res/rating_tag_counts_method4.csv','w')

for tag, score in tqdm(tags_and_escores):
	# print("{} {}".format(int(score), tag))
	(s, q, e) = tag_counts[tag]
	tags_file.write("{} {} {} {} {}\n".format(score, tag, s, q, e))

tags_file.close()

