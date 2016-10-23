'''
TODO

call downloader.download_all_info_vectors("id: {}".format(id)) for every image, because the filenames seemed to have been truncated
'''

def get_info_vectors():
    from os import listdir
    from os.path import isfile, join, splitext

    mypath = "res/images_mine"

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    tag_string_vectors = []

    for file in onlyfiles:
        filename, _ = splitext(file)
        tags = filename.split(" ")
        tag_string_vectors.append(tags)

    # print tag_string_vectors
    return tag_string_vectors


# for s in [get_info_vectors()[0]]:
for s in get_info_vectors():
    site = s[0]
    image_id = s[1]
    tags = s[2:]

    import downloader
    downloader.download_info("id:{}".format(image_id), filename="res/tags_mine/{}_{}.xml".format(site, image_id), site=site)



def plot_tags_quantities():
    lengths = [len(v) for v in get_info_vectors()]
    avg_length = 1.0*sum(lengths)/len(lengths)
    print("avg_length: {}".format(avg_length))

    import matplotlib.pyplot as plt
    x = [i for i in range(len(lengths))]
    plt.plot(x, lengths, 'ro')
    plt.axis([0, len(lengths), 0, 20])
    plt.show()

# plot_tags_quantities()


def print_top_tags():
    tag_string_vectors = get_info_vectors()
    flattened_tag_strings = [tag for v in tag_string_vectors for tag in v]

    x = flattened_tag_strings
    from collections import Counter
    counts = Counter(x)
    # for x in counts:
    #     print(x, counts[x])
    # print(str(counts))

    threshold = 10
    top_counts = [(k, v) for k, v in counts.iteritems() if v > threshold]
    top_counts = sorted(top_counts, key=lambda x: -x[1])
    top_counts = ["{}: {}".format(k,v) for k, v in top_counts]
    print("\n".join(top_counts))

# print_top_tags()

