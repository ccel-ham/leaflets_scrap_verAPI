import base64
from bs4 import BeautifulSoup
import config
import json
import re
import requests
import time

GOOGLE_URL = config.GOOGLE_URL
LINE_TOKEN = config.LINE_TOKEN
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

def get_image_base64(url):
    response = requests.get(url)
    image = response.content
    base64en = base64.b64encode(image)    
    base64data = base64en.decode('utf-8')
    return base64data, image

def get_leaflet_API():
    print("get-API...")
    response = requests.get(GOOGLE_URL)
    content = response.json()
    return content


def line_notify(shop, image):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ LINE_TOKEN}
    message = f"\n{shop}'s New Leaflet"
    payload = {"message" : message}
    files = {"imageFile": image}
    requests.post(url ,headers = headers ,params=payload,files=files)

def scraping_yama():
    #yamadaya
    url_header = "http://www.super-yamadaya.com/"
    url_footer = "sp/store/momoyama.html"
    url = url_header + url_footer
    headers = {'User-Agent': ''}
    res=requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    base64_list = {}
    image_list = {}
    class_name_list = ['ww45 left block', 'ww45 right block']
    i = 1
    for class_name in class_name_list:
        a_tag = soup.find('a', class_=class_name)
        img_tag = a_tag.find('img')
        _img = img_tag.get("src")
        img_url = url_header + _img.replace("../","")
        base64data, image = get_image_base64(img_url)
        base64_list[f"yamada-{i}"] = base64data
        image_list[f"yamada-{i}"] = image
        i += 1
    return base64_list, image_list


def scraping_Tokubai(name, url):
    #cosmo, matsumoto
    headers = {'User-Agent': USER_AGENT}
    res=requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    section_tag = soup.find('section', class_="branding_shop_component leaflet_component")
    img_tags = section_tag.find_all('img')
    base64_list = {}
    image_list = {}
    i = 1
    for img_tag in img_tags:
        img = img_tag.get("data-src")
        pattern = '/w=\d*,h=\d*,mc=true,wo=\d*,ho=\d*,cw=\d*,ch=\d*,aw=\d*/'
        result = re.search(pattern, img)
        str = result.group()
        img_url = img.replace(str, "/o=true/")
        base64data, image = get_image_base64(img_url)
        base64_list[f"{name}-{i}"] = base64data
        image_list [f"{name}-{i}"] = image
        i += 1
    return base64_list, image_list


def main():
    print("start...")
    start = time.time()
    base64_dict={}
    image_dict={}
    name_list = ["cosmo", "matsumoto"]
    shop_id_list = ["115207","44919"]
    TOKUBAI_URL = "https://tokubai.co.jp/"
    for name, shop_id in zip(name_list, shop_id_list):
        base64_dict[name], image_dict[name] = scraping_Tokubai(name, TOKUBAI_URL+shop_id)
    base64_dict["yamada"], image_dict["yamada"] = scraping_yama()
    api_dict = get_leaflet_API() 
    for key in api_dict.keys():
        post_to_LINE(key, api_dict[key], base64_dict[key], image_dict[key])
    post_to_update(base64_dict)
    print("...END")
    print(f"PROCCESSING TIME: {round(time.time()-start)} sec")

    return

def post_to_update(base64_dict):
    print("post-API...")
    data = json.dumps(base64_dict)
    response = requests.post(GOOGLE_URL, data=data)
    print(f"Response Code: {response.status_code} - {response.text}")


def post_to_LINE(shop, origin_dict, new_dict, image_dict):
    origin_value = origin_dict.values()
    new_value = new_dict.values()
    image_value = image_dict.values()        
    for new_base64, image in zip(new_value, image_value):
        if not new_base64 in origin_value:
            print(f"{shop} - UP DATE")
            line_notify(shop, image)
        else:
            print(f"{shop} - SAME")


if __name__=="__main__":
    main()

# In[ ]:




