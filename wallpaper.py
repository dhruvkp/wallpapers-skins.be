#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import requests
import urllib
import json
import subprocess
import os
from datetime import datetime
import shutil
import time

base_page_url="http://www.skins.be/tags/1440x900/page/"
resolution="1440x900"

SCRIPT = """/usr/bin/osascript<<END
tell application "System Events"
tell current desktop
set picture to "%s"
get properties
end tell
end tell
END"""



while True:
    config = open('/Users/dhruv/projects/wallpapers-skins.be/current_details','rb+')
    json_string = config.read()
    print json_string
    jsonobj = json.loads(json_string)

    last_time = datetime.strptime(jsonobj['time'],'%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.now()
    diff = current_time-last_time
    diff=float((diff.days * 86400 + diff.seconds)/60)

    if diff>0:

        try:
            page_url=base_page_url
            image_index = int(jsonobj['index'])
            page_index = int(jsonobj['page'])
            if page_index==1823:
                page_index=1
                image_index=1
            if image_index==10 or image_index==0:
                image_index=1
                page_index+=1
            else:
                image_index+=1
            page_url = base_page_url+str(page_index)+"/"
            print page_url
            page_html = requests.get(page_url).content
            soup = BeautifulSoup(page_html)
            images=soup.findAll('div',{'class':'motiveImage'})
            cnt=1
            for i in images:
                if cnt==image_index:
                    href=i.findChildren()[0]['href']
                    start_string=href[0:href.rfind('/',0,href.rfind('/',0,len(href)-1))]
                    code=href[href.rfind('/',0,href.rfind('/',0,len(href)-1))+1:href.rfind('/',0,len(href)-1)]
                    actress=start_string[start_string.rfind('/')+1:]
                    image_url="http://wallpapers.skins.be/"+actress+"/"+actress+"-"+resolution+"-"+code+".jpg"
                    print image_url
                    localpath="/Users/dhruv/projects/wallpapers-skins.be/background.jpg"
                    if os.path.exists(localpath):
                        urllib.urlretrieve(image_url,'/Users/dhruv/projects/wallpapers-skins.be/background2.jpg')
                        os.remove(localpath)
                        localpath="/Users/dhruv/projects/wallpapers-skins.be/background2.jpg"
                    else:
                        urllib.urlretrieve(image_url,'/Users/dhruv/projects/wallpapers-skins.be/background.jpg')
                        os.remove("/Users/dhruv/projects/wallpapers-skins.be/background2.jpg")
                    subprocess.Popen(SCRIPT%localpath, shell=True)
                    break
                else:
                    cnt+=1
                    continue
            config.seek(0)
            config.write('{"page":"'+str(page_index)+'","index":"'+str(image_index)+'","time":"'+str(datetime.now())+'"}')
            config.truncate()
            config.close()
            continue
        except:
            time.sleep(10)
            continue
    else:
        time.sleep(10)
