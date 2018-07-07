from bs4 import BeautifulSoup
import re


#dom = BeautifulSoup(open("tests/fixtures/www.fanfiction.net_1.html"), "html.parser")
dom = BeautifulSoup(open("tests/fixtures/www.fanfiction.net_1.html"), "lxml")

info_box = dom.select("#profile_top")[0]
info_fields = info_box.select(".xcontrast_txt")

author_name = info_fields[2]
title = info_fields[0]
summary = info_fields[5]
(score, updated, published, id) = re.findall(
    r'.*Favs:\s+([\d,]+).*Updated:.*?xutime="(\d+)".*?Published:.*?xutime="(\d+)".*?id:\s+(\d+)',
    str(info_fields[6]),
    re.DOTALL
)[0]

import ipdb; ipdb.set_trace()
