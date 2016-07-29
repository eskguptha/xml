import PyRSS2Gen
import datetime
import urllib
import re
from bs4 import BeautifulSoup
system_path = "1.xml"
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
items = []
for each in html_data:
	items.append(PyRSS2Gen.RSSItem(
     title = each['title'],
     link = "http://www.monmouth.edu/school-of-science/news-and-events.aspx#%s"%each['link'],
     description =  re.sub(r'[?|$|.|!]',r'',each['description']),
     guid = each['link'],
     ))
rss = PyRSS2Gen.RSS2(
    title = "Monmouth News Feed",
    link = "http://www.monmouth.edu/school-of-science/news-and-events.aspx",
    description = "Monmouth University News",
    generator = "PyRSS2Gen-1.1.0",
    docs = "http://blogs.law.harvard.edu/tech/rss",
    items = items
    )
rss.write_xml(open("%s"%system_path, "w"))