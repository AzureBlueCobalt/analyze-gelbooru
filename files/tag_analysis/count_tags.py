from bs4 import BeautifulSoup
import numpy as np
from collections import defaultdict
import time, datetime
from tqdm import tqdm
import dateutil.parser

tag_counts = []

# sample_size = 1E3
# sample_size = 10E3
# sample_size = 1*100E3
sample_size = -1

if sample_size == -1:
	sample_size = 3004112
with open("../all_gelbooru.xml", "r") as f:
	for i, line in tqdm(enumerate(f), total=sample_size):
		if i < sample_size:
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				id_num = int(post["id"])

				tags = post["tags"].strip().split(" ")

				num_tags = len(tags)
				tag_counts.append((num_tags, id_num))
		else:
			break

tag_counts = np.array(tag_counts)
from scipy import stats
# print(stats.describe(tag_counts))

tags_file = open('res/tag_counts.txt','w')
for tag_count in tqdm(tag_counts):
	tags_file.write("{}\n".format(tag_count))
tags_file.close()
