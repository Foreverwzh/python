"""
A test spider.
"""
# pylint: disable=invalid-name
# pylint: disable=line-too-long
import re
import os
import configparser
from io import BytesIO
import requests
import matplotlib.pyplot as plt
from PIL import Image

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'Host':'www.douban.com',
    'Upgrade-Insecure-Requests':'1'
}

def getCookies():
    """getCookies"""
    cf = configparser.ConfigParser()
    try:
        cf.read('conf.ini')
        cookies = cf.items('cookies')
        cookies = dict(cookies)
    except Exception as e:
        print('Exception: ' + e)
        cookies = {}
    return cookies

def getPage(r):
    """get all page links"""
    page_num = 0
    reg1 = re.compile('<span.*?class="thispage".*?data-total-page="(.*?)">.*?</span>')
    res = re.findall(reg1, r.text)
    if res:
        page_num = int(res[0])
    return page_num

def findTitle(url, pages, cookies):
    """find all title links"""
    t = []
    page = 0
    while page < pages:
        u = url+'?start='+str(page*25)
        print('Connecting to "'+u+'":')
        r = requests.get(u, headers=header, cookies=cookies)
        if r.status_code == 200:
            print('Success')
            reg = re.compile(r'<td\s*class="title"\s*?>\s*?<a href="(.*?)".*?>.*?</a></td>', re.S|re.M)
            titles = re.findall(reg, r.text)
            t += titles
        elif r.status_code == 403:
            c = humanProve(r, u)
            if not c:
                print('403')
                exit()
        else:
            print(r.status_code)
        page += 1
    return t

def downloadImage(imgurls, cookies):
    """download image"""
    for i in imgurls:
        print('Downloading '+i+':')
        r = requests.get(i, stream=True, cookies=cookies)
        if r.status_code == 200:
            size = 0
            if not os.path.exists('cat/img'):
                os.mkdir("cat/img")
            path = 'cat/img/'+i.split('/')[-1]
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
                    size += 1
            print('Success')
            if size < 50:
                os.remove(path)
                print('Delete '+i)
        else:
            print('Error')

def humanProve(r, originalurl):
    """ hunman being proving """
    pattern = re.compile(r'<img src="(.*?)" alt="captcha"/>')
    res = re.findall(pattern, r.text)
    if res:
        r = requests.get(res[0])
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            plt.figure("captcha")
            plt.imshow(img)
            plt.show()
            c_str = input('Please input captcha string: ')
            cid = res[0].replace('https://www.douban.com/misc/captcha?id=', '')
            print(cid)
            data = {
                'ck': 'QLVZ',
                'captcha-solution': c_str,
                'captcha-id': cid,
                'original-url': originalurl
            }
            print(data)
            rp = requests.post('https://www.douban.com/misc/sorry', data=data, cookies=getCookies(), headers=header)
            if rp.status_code == 403:
                humanProve(rp, originalurl)
            elif rp.status_code == 200:
                return rp
            else:
                print(rp.status_code)
                return False
        else:
            print("Fail to download captcha image.")
            return False
    else:
        return False

def showImage(path):
    """ show image """
    img = Image.open(path)
    plt.figure(path)
    plt.imshow(img)
    plt.show()

def main():
    """main function"""
    url = 'https://www.douban.com/group/481977/discussion'
    cookies = getCookies()
    r = requests.get(url, headers=header, cookies=cookies)
    if r.status_code != 200:
        if r.status_code == 403:
            r = humanProve(r, url)
            if not r:
                print('403')
                exit()
        else:
            print(r.status_code)
            exit()
    print('Page_links:')
    pages = getPage(r)
    print(pages)
    if not pages:
        exit()
    print('Title_url:')
    titles_url = findTitle(url, pages, cookies)
    print(len(titles_url))
    for title_url in titles_url:
        print('Connecting to "'+title_url+'":')
        r = requests.get(title_url, headers=header, cookies=cookies)
        if r.status_code == 200:
            print('Success')
            reg1 = re.compile('<body>(.*?)</body>', re.M|re.S)
            body = re.findall(reg1, r.text)[0]
            reg2 = re.compile('<div.*?class="topic-figure cc">.*?<img.*?src="(.*?)".*?>.*?</div>', re.M|re.S)
            img_arr = re.findall(reg2, body)
            new_arr = []
            for i in img_arr:
                a = re.match(r'[a-zA-z]+://[^\s]*', i)
                if a is not None:
                    new_arr.append(i)
            print(new_arr)
            downloadImage(new_arr, cookies)
        else:
            print('Error: ' + str(r.status_code))
            if r.status_code == 403:
                humanProve(r, title_url)
            else:
                exit()
    print('All titles: ' + str(len(titles_url)))
# main()

if __name__ == '__main__':
    main()
