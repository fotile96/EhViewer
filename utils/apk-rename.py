import json
import os

os.chdir(__file__.replace('utils\\apk-rename.py', 'app\\release\\'))

meta = json.load(open('output-metadata.json', 'r'))

for ele in meta['elements']:
    name_old: str = ele['outputFile']
    name_new: str = name_old.replace('app', 'EhViewer').replace('release', '')
    name_new = name_new.replace('.apk', f'v{ele["versionName"]}.apk')
    try:
        os.rename(name_old, name_new)
        print(name_new)
    except:
        pass
