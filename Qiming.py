from bs4 import BeautifulSoup
import requests

#姓氏
generalLastName = "王"

# print(res.url)
# print(soup.prettify())

#通过姓获取名数组
def fetchNamesWithLastNameAndPage(lastName, page):
    qimingUrl = "http://m.sheup.com/mianfeiqiming.php"
    params = {"qiming": lastName.encode('gb2312'), "setsex": "boy", "setming": "0", "Submit": "免费在线起名".encode('gb2312'), "page":page}
    res = requests.post(url=qimingUrl, data=params)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "lxml")
    nameDiv = soup.find("div", {"class": "name_main"})
    # 抓取名字
    nameList = []
    for litag in nameDiv.ul.children:
        if (litag.string.strip() != ""):
            nameList.append(litag.string)
    return nameList

#通过姓名获得得分
def fetchMarkWithLastNameAndLastName(lastName, firstName):
    ceshiUrl = "http://m.sheup.com/xingming_ceshi_1.php"
    params = {"ceshi_xing": lastName.encode("gb2312"), "ceshi_ming": firstName.encode("gb2312"),
                   "dafen": "姓名测试打分".encode("gb2312")}
    res = requests.post(url=ceshiUrl, data=params)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "lxml")
    subMainDiv = soup.find("div", {"class": "subs_main"})
    return subMainDiv.p.font.string

def lastNameAndFirstName(name, lastName):
    lastNameLen = len(lastName)
    firstName = name[lastNameLen:]
    return lastName, firstName


page = 1
while 1:
    nameList = fetchNamesWithLastNameAndPage(generalLastName, page)
    if len(nameList) != 0:
        for name in nameList:
            lastName, firstName = lastNameAndFirstName(name, generalLastName)
            mark = fetchMarkWithLastNameAndLastName(lastName, firstName)
            if int(mark) >= 95:
                print(name + " " + mark)
        page += 1
    else:
        break;