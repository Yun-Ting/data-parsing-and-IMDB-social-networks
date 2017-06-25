import time
import json

import pydot
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import itertools
reload(sys)
sys.setdefaultencoding('utf-8')


# response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100')
# html_doc = response.read()
#
# step1_file = open("step1_output.html", "w")
# for line in html_doc:
#     step1_file.write(line)
# step1_file.close()

# step1
soup = BeautifulSoup(open("step1_output.html"),"html.parser")
body_tag = soup.body
each_of_100_list = soup.find_all("div", {"class":"lister-item mode-advanced"})
before_processed_list = []

# step2
step2_file = open("step2_output.txt", "w")
for row in each_of_100_list:
    # a = row.find(re.compile("/title/(.*)/\?ref_=adv_li_tt"))
    pro_year = row.find("span", {"class": "lister-item-year text-muted unbold"})
    match = re.search("/title/(.*)/\?ref_=adv_li_tt", row.h3.a.get('href'))
    processed = match.group(1)
    step2_file.write(processed + "\t" + row.h3.span.string[:-1] + "\t" + row.h3.a.string + " " + pro_year.string + '\n')
step2_file.close()

# step3
# f = open("step2_output.txt","r")
# step3_file = open("step3_output.txt", "w")
# for line in f:
#     id = line.split("\t")[0]
#     step3_file.write(urllib2.urlopen("http://www.omdbapi.com/?i={}&plot=full&r=json".format(id)).read() + '\n')
#     time.sleep(5)
# step3_file.close()

# step4
f = open("step3_output.txt","r")
step4_file = open("step4_output.txt", "w")

graph = pydot.Dot(graph_type="graph", charset = "utf8")
for movie in f:
    movie_obj= json.loads(movie)
    actor_list= movie_obj["Actors"].split(", ")
    step4_file.write(movie_obj["Title"] + "\t" +json.dumps(actor_list[:5]) + "\n")
    # step5
    co_actor_list = list(itertools.combinations(actor_list ,2))
    for actor_pair in co_actor_list:
        edge = pydot.Edge(json.dumps(actor_pair[0]),json.dumps(actor_pair[1]))
        graph.add_edge(edge)
graph.write("actors_graph_output.dot")
step4_file.close()

