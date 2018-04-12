import configparser
import os, re
import requests
from bs4 import BeautifulSoup
from cookieEditter import getEtutorCookies

# init setting
# setting download folder Path
config = configparser.ConfigParser()
config.read('profile.ini')
folderPath = config['path']['folderpath']
try:
    os.makedirs(folderPath, mode=0o777)
except OSError:
    pass
finally:
    print("下載的檔案會在" + folderPath + "資料夾中")

# setting login user profile and cookie
user = config['user']
username = user['username']
password = user['password']

# setting target crawler page
targetPageUrl = config['target']['targetURL']

# Etutor
# 1' get etutor session
etutorURL = "http://e-tutor.itsa.org.tw/e-Tutor/"
etutorHOME = requests.request("get", etutorURL)

# 2' visible target cookies
etutorCookies = etutorHOME.headers.get('Set-Cookie')
etutorCookies = getEtutorCookies(etutorCookies)

# 3' login with etutorCookie headers
etutorLoginURL = "http://e-tutor.itsa.org.tw/e-Tutor/login/index.php"
_headers = {"Cookie": etutorCookies[0] + etutorCookies[1] + etutorCookies[2]}
_formData = ({"username": username, "password": password})
requests.post(etutorLoginURL, data=_formData, headers=_headers, allow_redirects=False)

# 4' targetPage
# targetPageUrl = "http://e-tutor.itsa.org.tw/e-Tutor/mod/programming/reports/best.php?a=22009"
targetPage = requests.get(targetPageUrl, headers=_headers)
targetSoup = BeautifulSoup(targetPage.text, 'html.parser')
title = targetSoup.find('title').text
title = str(re.sub('(\#|\%|\&|\*|\||\\\|\:|\"|\<|\>|\?|\/)', ' ', title))
savePath = folderPath + title + ".txt"


# 5' get all target and save it
# we have more then one page so we need to change page
while True:
    # 6 get target source code page
    targetTable = targetSoup.find("div", attrs={"class": "maincontent2"})
    # find all target <tr class="r0"> and <tr class="r1">
    targets = targetTable.find_all("tr", attrs={"class": re.compile('r0|1')})
    for target in targets:
        targetTime = target.find("td", attrs={"class": "cell c1"}).text
        targetName = target.find("td", attrs={"class": "cell c2"}).text
        # print(target.find("td", attrs={"class": "cell c3"}).text + " ")
        sourceCodePageUrl = target.find("td", attrs={"class": "cell c4"}).a.get('href')

        # 7' get source code
        sourceCodePage = requests.get(sourceCodePageUrl, headers=_headers)
        sourceCodePageSoup = BeautifulSoup(sourceCodePage.text, 'html.parser')
        sourceCode = sourceCodePageSoup.find("textarea").text
        with open(savePath, 'a') as f:
            f.write(targetName+"\n")
            f.write(targetTime+"\n")
            f.write(sourceCode+"\n")
            f.write("*******"+"\n")

    nextPage = targetTable.find("a", attrs={"class": "next"})
    if nextPage is not None:
        nextPageUrl = nextPage.get('href')
        targetPage = requests.get(nextPageUrl, headers=_headers)
        targetSoup = BeautifulSoup(targetPage.text, 'html.parser')
    else:
        break

# ending
print('end')