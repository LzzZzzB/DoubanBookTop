import json
from multiprocessing import Pool
import requests
import re
from requests import RequestException


def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        response = requests.get(url,headers)
        if response.status_code == 200:

            print(response.text)
        return (response.text)
    except RequestException:
        print("Request出错啦！")


def parse_url(content):
    pattern = re.compile('<li.*?subject-item.*?<a\sclass="nbg"\shref="(.*?)".*?src="(.*?)".*?title="(.*?)".*?pub">(.*?)</div>'
                         +'.*?pl">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern,content)
    print (items)
    print (len(items))
    for item in items:
        yield{
            'title': item[2],
            'author': item[3].strip(),
            'comment': item[4].strip(),
            'url': item[0],
            'image': item[1]
        }


def write_to_file(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main(num):
    url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start="+ str(num) + "&type=T"
    content = get_url(url)
    parse_url(content)
    for item in parse_url(content):
        print(item)
        write_to_file(item)

if __name__ == "__main__":
    pool = Pool()
    pool.map(main,[i*20 for i in range(8)])