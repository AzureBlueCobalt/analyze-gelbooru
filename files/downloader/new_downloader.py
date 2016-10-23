from bs4 import BeautifulSoup
# from urllib2 import urlopen #python 2
from urllib.request import urlopen #python 3
import time
import datetime
import re
import urllib
import sys


total_number_of_images = 3227131


def make_query(query, site="safebooru.org", images_per_page=10, page_id=0):
    tags = query.split(" ")
    html_doc = urlopen("http://{}/index.php?page=dapi&s=post&q=index&pid={}&tags={}&limit={}".format(site, page_id, "+".join(tags), images_per_page))
    html_doc = html_doc.read()
    return html_doc


def get_number_of_matches(query, site="safebooru.org"):
    html_doc = make_query(query, site=site, images_per_page=0)
    soup = BeautifulSoup(html_doc, "lxml")
    posts = soup.find("posts")
    if posts is not None:
        total_images = int(posts.get("count"))
        return total_images
    else:
        return -1

# num = get_number_of_matches("hikage_eiji open_mouth", "gelbooru.com")
# print(num)


def download_info(query, filename="query_results.xml", site="safebooru.org", limit=-1, images_per_page=40):
    with open(filename, "w") as results_file:
        if limit == -1:
            limit = get_number_of_matches(query, site)

        page_id = 0
        images_downloaded = images_per_page*page_id#0

        while images_downloaded < limit:
            # time.sleep(4)

            a = images_downloaded+1
            b = images_downloaded+images_per_page
            completion = 100.0*images_downloaded/limit

            #TODO: make this write directly to a log file
            print("downloading images {} - {} / {} = {:.2f}% (page {})".format(a, b, limit, completion, page_id))

            html_doc = make_query(query, site=site, images_per_page=images_per_page, page_id=page_id)

            soup = BeautifulSoup(html_doc, "lxml")

            every_post = soup.findAll("post")
            # print(every_post)
            for post in every_post:
                # print(post)
                results_file.write(str(post))
                results_file.write("\n")


            images_downloaded += images_per_page
            page_id += 1


# import time
# start_time = time.time()
# # download_info("id:<1644354", site="gelbooru.com", images_per_page=950)
# # download_info("*", site="gelbooru.com", limit=1500000, images_per_page=950)
# # download_info("hikage_eiji open_mouth", site="safebooru.org")
# # download_info("hikage_eiji open_mouth", site="gelbooru.com")
# print("--- %s seconds ---" % (time.time() - start_time))


def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def download_sample_for_info_vector(info_vector):
    # print(info_vector)

    # get the id of the entry
    m = re.search(r'\sid="(\d+)"\s', info_vector)
    image_id = int(m.group(1)) if m else -1
    # print("id: {}".format(image_id))


    # if image_id % 1 == 0:
    if image_id % 100 == 0:
        completion = 100.0-(100.0*image_id/total_number_of_images)
        print("[{}] downloading id {} of {} = {:.4f}%".format(timestamp(), image_id, total_number_of_images, completion))
        sys.stdout.flush()


    # get the url for the sample image (the smallest one, of course)
    m = re.search(r'\spreview_url="([^\"]+)"\s', info_vector)
    preview_url = m.group(1) if m else ""
    # print("preview_url: {}".format(preview_url))

    # get the file extension
    extension = preview_url[preview_url.rfind("."):]

    # download the sample image and set the filename to be the image id (0 padded)
    try:
        testfile = urllib.URLopener()
        testfile.retrieve(preview_url, "res/images_all/{:09d}{}".format(image_id,extension))
    except:
        with open("downloader.py.log", "a") as error_log:
            error_log.write("[{}] ==DOWNLOAD FAILED== id:'{}' url:'{}'\n".format(timestamp(), image_id, preview_url))


# info_vector = """<post change="1445066068" created_at="Mon Jul 16 00:20:03 -0500 2007" creator_id="6498" file_url="http://simg4.gelbooru.com/images/e5/b4/e5b4230a704b21ccadda4cd6f07104c0.jpg" has_children="false" has_comments="true" has_notes="false" height="550" id="11" md5="e5b4230a704b21ccadda4cd6f07104c0" parent_id="" preview_height="150" preview_url="http://gelbooru.com/thumbnails/e5/b4/thumbnail_e5b4230a704b21ccadda4cd6f07104c0.jpg" preview_width="107" rating="s" sample_height="550" sample_url="http://simg4.gelbooru.com/images/e5/b4/e5b4230a704b21ccadda4cd6f07104c0.jpg" sample_width="395" score="5" source="" status="active" tags=" 2boys androgynous bad_anatomy bare_shoulders brown_hair fuuchouin_kazuki getbackers kakei_juubei long_hair low-tied_long_hair male_focus multiple_boys rotational_symmetry short_hair trap yaoi yellow_eyes " width="395"></post>"""
# download_sample_for_info_vector(info_vector)

print("="*10+"program starting"+"="*10)

print("finding id of last image downloaded...")
sys.stdout.flush()


def get_last_downloaded_id():
    #first try the fast way, by reading the progress log
    print("using log file to find id...")
    sys.stdout.flush()
    with open('image_downloading_status', 'r') as myfile:
        data = myfile.read()

        last_lines = reversed(data.split('\n')[-20:])
        last_download = next(x for x in last_lines if len(x) > 0 and x[0]=='[')
        last_match = re.search('id (\d+) of', last_download)
        if last_match:
            last_id_downloaded = int(last_match.group(1))
            return last_id_downloaded

    #if that fails, try the slow way by checking all images downloaded so far
    print("previous method failed.\nreading image directory...")
    sys.stdout.flush()
    mypath = "res/images_all"
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    last_image_downloaded = onlyfiles[-1]
    last_id_downloaded = int(last_image_downloaded[:last_image_downloaded.rfind(".")])
    return last_id_downloaded

last_id_downloaded = get_last_downloaded_id()
print("last id was {}".format(last_id_downloaded))

print("skipping files...")
sys.stdout.flush()

starting_index = total_number_of_images-last_id_downloaded
# for each entry in "res/tags_all/all_gelbooru.xml"
with open("res/tags_all/all_gelbooru.xml", "r") as all_info_vectors:

    from tqdm import *
    print("skipping already-downloaded images...")
    sys.stdout.flush()
    for i in tqdm(range(starting_index)):
        next(all_info_vectors)

    print("resuming download...")
    sys.stdout.flush()
    for info_vector in all_info_vectors:
        download_sample_for_info_vector(info_vector)

print("="*10+"program ending"+"="*10)


#make a space where every dimension is is a unique tag found in downloaded tags
def create_vector_space():
    pass

#parse a string vector into a bit vector represented in the vector space created by the function above
def info_vector_to_bit_vector(string_vector):
    pass
