import requests
import re
import os

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'Host':'www.douban.com',
    'Upgrade-Insecure-Requests':'1'
}

def login():
    url = 'https://accounts.douban.com/login'

def getPage(r):
    reg1 = re.compile('<div.*?class="paginator".*?>(.*?)</div>',re.S|re.M)
    res = re.findall(reg1, r.text)
    if len(res) != 0:
        html = res[0]
        reg2 = re.compile('<a.*?href="(.*?)".*?>\d+</a>',re.S|re.M)
        url_arr = re.findall(reg2, html)
        return url_arr
    else:
        return []


def findTitle(pages):
    t = []
    for page in pages:
        print('Connecting to "'+page+'":')
        r = requests.get(page, headers = header)
        if r.status_code==200:
            print('Success')
            reg = re.compile('<td\s*class="title"\s*?>\s*?<a href="(.*?)".*?>.*?</a></td>',re.S|re.M)
            titles = re.findall(reg, r.text)
            print(titles)
            t+=titles
        else:
            print('Error')
    return t



def downloadImage(imgurls):
    for i in imgurls:
        print('Downloading '+i+':')
        r = requests.get(i,stream = True)
        if r.status_code==200:
            size = 0
            path = '/cat/img/'+i.split('/')[-1]
            with open(path,'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
                    size+=1
            print('Success')
            if size<50:
                os.remove(path)
                print('Delete '+i)
        else:
            print('Error')



url = 'https://www.douban.com/group/417139/discussion'
r = requests.get(url,headers = header)
if r.status_code!=200:
    print(r.status_code)
    exit()
print('Page_links:')
pages = getPage(r)
print(pages)
print('Title_url:')
titles_url = findTitle(pages)
print(titles_url)
for title_url in titles_url[:30]:
    print('Connecting to "'+title_url+'":')
    r = requests.get(title_url,headers = header)
    if r.status_code==200:
        print('Success')
        reg = re.compile('<img src="(.*?)"')
        img_arr = re.findall(reg, r.text)
        new_arr = []
        for i in img_arr:
            a = re.match(r'[a-zA-z]+://[^\s]*',i)
            if a is not None:
                new_arr.append(i)
        print(new_arr)
        downloadImage(new_arr)
    else:
        print('Error')