import requests
import bs4
from bs4 import BeautifulSoup
from xlwt import *

url = "https://flights.ctrip.com/schedule/departairport-jiangbei"
appendix = "/inmap.html"
planelist = []

def clear_info(str):
    final = str.replace("<br/>", "")
    final = final.replace("<br>", "")
    final = final.replace("</br>", "")
    final = final.replace("</td>", "")
    final = final.replace("<td>", "")
    final = final.replace(" ", "")
    return final
def check_jiangbei_page(appendix):
    r = requests.get(url+appendix)
    if(r.status_code == 200):
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        for tr in soup.find('tbody').children:
            if(isinstance(tr, bs4.element.Tag)):
                tds = tr('td')
                s1 = str(tds[0])
                s2 = str(tds[1])
                s1_r = clear_info(s1)
                s2_r = clear_info(s2)
                planelist.append([s1_r, s2_r])

for i in range(99):
    if(i == 0):
        appendix = "/inmap.html"
        check_jiangbei_page(appendix)
    else:
        appendix = "/inmap-" + str(i+1) + ".html"
        check_jiangbei_page(appendix)

# for i in range(len(planelist)):
#     print(planelist[i][0], planelist[i][1])

file = Workbook(encoding = 'utf-8')
table = file.add_sheet('data')

for i in range(len(planelist)):
    m = []
    start, end = planelist[i][0].split()
    stime, etime = planelist[i][1].split()
    m.append(start)
    m.append(end)
    m.append(stime)
    m.append(etime)
    for j in range(4):
        table.write(i, j, label = m[j])

file.save("test2.xls")