import requests
from lxml import etree
import os
import re

'''
host_list = ['github.com', 'api.github.com', 'avatars1.githubusercontent.com',
             'avatars2.githubusercontent.com', 'github.githubassets.com', 'raw.githubusercontent.com']
'''
host_list = ['exhentai.org', 'e-hentai.org', 'repo.e-hentai.org',
             'forums.e-hentai.org', 'ehgt.org', 'ul.ehgt.org']


baseUrl = 'https://ipchaxun.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

results = {'': '\n\n# C:\\Windows\\System32\\drivers\\etc\\HOSTS\n# /etc/hosts\n'}

for host in host_list:
    r = requests.get(baseUrl + host, headers=headers)
    print(r, host)
    r = etree.HTML(r.text).xpath('//span[@class="date"]/../a/text()')
    print(f'ping test of  "{host}"  start...')
    results[host] = [(ip, os.popen(f'ping {ip}')) for ip in r[:16]]  # 只保留较新的记录


def filter(host, ip, log):
    log = re.findall(r'=([0-9]+ms) TTL=', log.read())
    if len(log) < 3:
        return ''
    else:
        for _ in range(4-len(log)):
            log.append('fail')
        return f'{ip} {host} # {",".join(log)}\n'


for host in host_list:
    results[host] = ''.join(filter(host, ip, log) for ip, log in results[host])
    results[host] += f"# {'+'.join(re.findall(r'[0-9]+.[0-9]+.[0-9]+.[0-9]+', results[host]))}\n"
    print(f'ping test of  "{host}"  finish.')


results = '\n'.join(results.values())
print(results)

os.chdir(__file__.replace('ipchaxun.py', ''))

with open('hosts.txt', 'a') as f:
    f.write(results)
