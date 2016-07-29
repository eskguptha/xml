import urllib
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import re
system_path = "/export/home/hawkdom2/s1087983/public_html/"
r = urllib.urlopen('http://www.monmouth.edu/academics/CSSE/news.asp').read()
soup = BeautifulSoup(r)
d = soup.find("div", id="ctl00_ctl00_baseMain_main_dzUpper_columnDisplay_ctl00_controlcolumn_ctl00_WidgetHost_WidgetHost_widget_CB")
d = str(d)
data =  d.split('<hr/>')
html_data = []
for each in data[1:]:
    bobj = BeautifulSoup(each)
    name_obj  = bobj.find('strong')
    name = ''
    if name_obj:
        name = name_obj.text

    c = bobj.find('a', class_='anchorMargin')
    click_url = ''
    if c:
        click_url = c['name']
    description  = bobj.find_all('p')
    if description:
        description = description[2].text
    else:
        description = ''
    if name:
        html_data.append({'title':name, 'link': click_url,'description':description[:140]})

root = ET.Element("channel")
head = ET.SubElement(root, "title")
head.text = "Monmouth News Feed"
link1 = ET.SubElement(root, "link")
link1.text = "http://www.monmouth.edu/school-of-science/news-and-events.aspx"
description1 = ET.SubElement(root, "description")
description1.text = "Monmouth University News"
generator_1 = ET.SubElement(root, "generator")
generator_1.text = "PyRSS2Gen-1.1.0"
docs1 = ET.SubElement(root, "docs")
docs1.text = "http://blogs.law.harvard.edu/tech/rss"
for each in html_data:
    doc = ET.SubElement(root, "item")
    ET.SubElement(doc, "title").text = each['title']
    ET.SubElement(doc, "link").text = each['link']
    ET.SubElement(doc, "description").text = each['description']
    tree = ET.ElementTree(root)
    tree.write("%scssenews.rss.xml"%system_path)
