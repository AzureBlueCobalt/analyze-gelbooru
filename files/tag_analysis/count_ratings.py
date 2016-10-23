from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle
from collections import defaultdict
from tqdm import tqdm

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

num_safe = 0
num_questionable = 0
num_explicit = 0

with open("../all_gelbooru.xml", "r") as f:
# with open("../some_gelbooru.xml", "r") as f:
	for i, line in enumerate(f):
		if i >= 0:
			if i % 1000 == 0:
				print("[{}] processing item {:07} / 3000000".format(timestamp(), i))
			# print(line)
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			if post is not None:
				rating = post["rating"]
				# print(rating)

				if rating == "s":
					num_safe += 1
				elif rating == "q":
					num_questionable += 1
				elif rating == "e":
					num_explicit += 1

total = num_safe + num_questionable + num_explicit

print("num_safe: {} ({:.2f}%)".format(num_safe, 100.0*num_safe/total))
print("num_questionable: {} ({:.2f}%)".format(num_questionable, 100.0*num_questionable/total))
print("num_explicit: {} ({:.2f}%)".format(num_explicit, 100.0*num_explicit/total))

