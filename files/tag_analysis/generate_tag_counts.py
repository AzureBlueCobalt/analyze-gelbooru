from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

tag_counts = defaultdict(int)

with open("../all_gelbooru.xml", "r") as f:
# with open("../some_gelbooru.xml", "r") as f:
	for i, line in enumerate(f):
		if i >= 0:
			if i % 1000 == 0:
				print("[{}] processing item {:07} / 3000000  unique tags: {}".format(timestamp(), i, len(tag_counts)))
			# print(line)
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				tags = post["tags"].strip().split(" ")
				# print(tags)

				for tag in tags:
					tag_counts[tag] += 1


tags_file = open('counts.csv','w')

for w in tqdm(sorted(tag_counts, key=tag_counts.get, reverse=True)):
	tags_file.write("{:07} {}\n".format(tag_counts[w], w))
    # print w, tag_counts[w]

tags_file.close()
