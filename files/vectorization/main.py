'''
read in some_gelbooru.xml
parse lines
compute vector space
vectorize all entries


ml 1
decision tree: tags -> rating

ml 2
regression tree: tags -> score

data 3:
filter out questionable
what terms are the most explicit, and what are the most safe?

'''
from bs4 import BeautifulSoup
import time, datetime
import numpy as np
import pickle

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

load_tag_map = True #if false create tag map, if true load tag map from file
tag_map_filename = "tag_map.p"
tag_map = dict()
num_tags = 0

if load_tag_map:
	with open(tag_map_filename, 'rb') as handle:
		(tag_map, num_tags) = pickle.loads(handle.read())
else:
	#make a set of all the tags
	all_tags = set()

	with open("all_gelbooru.xml", "r") as f:
	# with open("some_gelbooru.xml", "r") as f:
		for i, line in enumerate(f):
			if i >= 0:
				if i % 1000 == 0:
					print("[{}] processing item {} / 3000000  unique tags: {}".format(timestamp(), i, len(all_tags)))
				# print(line)
				soup = BeautifulSoup(line, "lxml")
				post = soup.find("post")
				if post is not None:
					tags = post["tags"].strip().split(" ")
					# print(tags)

					all_tags.update(tags)

	#make the vector space
	all_tags = list(all_tags)
	num_tags = len(all_tags)

	for i, tag in enumerate(all_tags):
		tag_map[tag] = i

	#save the tag map to a file (so it can be reloaded later)
	data = (tag_map, num_tags)
	with open(tag_map_filename, 'wb') as handle:
		handle.write(pickle.dumps(data))
		
	#DEBUG
	#DEBUG
	#DEBUG
	exit()
	#DEBUG
	#DEBUG
	#DEBUG




#function to turn a array of tags into a boolean vector
def vectorize(tags):
	vector = [False]*num_tags
	vector = np.array(vector)
	for tag in tags:
		index = tag_map[tag]
		vector[index] = True
	return vector


#clear the vectorized_tags file
tags_file = open('vectorized_tags.csv','w')
tags_file.write("")
tags_file.close()


#fill up the vectorized_tags file
tags_file = open('vectorized_tags.csv','w')

with open("some_gelbooru.xml", "r") as f:
	for i, line in enumerate(f):
		if i < 1:
			# print(line)
			soup = BeautifulSoup(line, "lxml")
			post = soup.find("post")
			tags = post["tags"].strip().split(" ")
			# print(tags)
			tag_vector = vectorize(tags)
			# print(tag_vector)
			# print(tag_vector.astype(int))
			to_write = "".join([str(x) for x in tag_vector.astype(int)]) + "\n"
			tags_file.write(to_write)


tags_file.close()



# print(all_tags)
