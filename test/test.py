#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: test.py
@time: 2018/1/15 下午5:09

"""
import requests

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36',
           'Accept': 'application/vnd.github.mercy-preview+json'
           }
# 文档地址
search_doc = 'https://developer.github.com/v3/search/'
url_base = 'https://api.github.com'
url_search_repository = '/search/repositories'


def get(url, char_set='utf-8'):
    session = requests.session()

    resp = session.get(url, headers=headers, stream=True, verify=False)
    resp.encoding = char_set
    return resp


def get_json(url):
    resp = get(url)
    if 200 == resp.status_code:
        try:
            j = resp.json()
            if isinstance(j, dict):
                j['code'] = 200
                j['url'] = url
                return j
        except Exception as e:
            print(e)
    return {'code': resp.status_code, 'url': url}


def repository_json(q, sort='stars', order='desc'):
    url = '{url_base}{url_search_repository}?q={q}&sort={sort}&order={order}'.\
        format(url_base=url_base, url_search_repository=url_search_repository, q=q, sort=sort, order=order)
    j = get_json(url)
    return j


def get_query(language, stars):
    return 'language:{}+stars:>={}'.format(language, stars)


def repository_search(language, stars=0):
    return repository_json(q=get_query(language, stars))


def main():
    j = repository_search(language='python', stars=1000)
    print(j['code'])
    print(j['url'])
    print(j['total_count'])


if __name__ == '__main__':
    main()
