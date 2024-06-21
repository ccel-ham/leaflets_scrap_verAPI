import base64
import hashlib
import io
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image


class TokubaiBot:
    def __init__(self, shop_name, shop_id, line_notify_token):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.url = f'https://tokubai.co.jp/{shop_id}'
        self.line_notify_token = line_notify_token
        self.post_flag = False
        self.image_storage = {}
        self.counter = 1

    def get_leaflet_images(self):
        response = self.get_main_requests()
        image_tags = self.find_image_tags(response)
        image_url_list = self.image_url_parser(image_tags)
        self.store_in_image_base64_hash(image_url_list)

    def get_main_requests(self):
        headers = {'User-Agent': self.user_agent}
        res = requests.get(self.url, headers=headers)
        return res

    def find_image_tags(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        section_tag = soup.find(id="leaflet")
        if section_tag:
            image_tags = section_tag.find_all('img')
        else:
            image_tags = []
        return image_tags

    def image_url_parser(self, image_tags):
        fullsize_image_list = []
        for image_tag in image_tags:
            image_url = image_tag.get("data-src")
            if image_url:
                pattern = '/w=\d*,h=\d*,mc=true,wo=\d*,ho=\d*,cw=\d*,ch=\d*,aw=\d*/'
                result = re.search(pattern, image_url)
                if result:
                    image_size_string = result.group()
                    fullsize_image_url = image_url.replace(
                        image_size_string, "/o=true/")
                    fullsize_image_list.append(fullsize_image_url)
        return fullsize_image_list

    def store_in_image_base64_hash(self, url_list):
        for url in url_list:
            response = requests.get(url)
            image = response.content
            base64en = base64.b64encode(image)
            base64data = base64en.decode('utf-8')
            image_hash = self.calculate_hash(base64en)
            storage_key = f'{self.shop_name}-{self.counter}'
            self.image_storage[storage_key] = {
                'image': image, 'base64': base64data, 'hash': image_hash}
            self.counter += 1
        return None

    def calculate_hash(self, image_data):
        sha1_hash = hashlib.sha1(image_data)
        image_hash = sha1_hash.hexdigest()
        return image_hash

    def new_leaflet_post_to_line(self, stored_hash_list):
        # self.image_storage[storage_key] = {'image':image, 'base64': base64data, 'hash':image_hash}
        for key in self.image_storage.keys():
            image_data = self.image_storage[key]
            if self.leaflet_update_check(image_data["hash"], stored_hash_list):
                print(f"post to LINE {key}")
                post_message = f"\n{self.shop_name}'s New Leaflet"
                post_image = self.compress_image_under_3MG_bytes(
                    image_data["image"])
                self.line_notify(post_message, post_image)

    def leaflet_update_check(self, leaflet_hash, stored_hash_list):
        if leaflet_hash in stored_hash_list:
            print(f"{self.shop_name} - SAME")
            return False
        else:
            print(f"{self.shop_name} - UP DATE")
            self.post_flag = True
            return True

    def line_notify(self, message, image):
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": "Bearer " + self.line_notify_token}
        payload = {"message": message}
        files = {"imageFile": image}
        res = requests.post(url, headers=headers, params=payload, files=files)
        if res.status_code >= 300:
            print(f"{res.text}")

    def compress_image_under_3MG_bytes(self, image_data, target_size=3):
        quality = 100
        image_io = io.BytesIO(image_data)
        image = Image.open(image_io)
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality)
        output.seek(0)
        while len(output.getvalue()) / (1024 * 1024) > target_size:
            quality -= 1
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality)
            output.seek(0)
        return output.getvalue()

    def output_base64_dictionary(self):
        output_dict = {}
        for key in self.image_storage.keys():
            image_data = self.image_storage[key]
            output_dict[key] = image_data["base64"]
        return output_dict


class YamadaBotCustomTokubai(TokubaiBot):
    def __init__(self, shop_name, line_notify_token):
        self.shop_name = shop_name
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.url_header = "http://www.super-yamadaya.com/"
        self.url = f"{self.url_header}sp/store/momoyama.html"
        self.line_notify_token = line_notify_token
        self.post_flag = False
        self.image_storage = {}
        self.counter = 1

    def find_image_tags(self, response):
        image_tags = []
        soup = BeautifulSoup(response.text, "html.parser")
        class_name_list = ['ww45 left block', 'ww45 right block']
        for class_name in class_name_list:
            a_tag = soup.find('a', class_=class_name)
            if a_tag:
                image_tag = a_tag.find('img')
                if image_tag:
                    image_tags.append(image_tag)
        return image_tags

    def image_url_parser(self, image_tags):
        image_url_list = []
        for image_tag in image_tags:
            image_src = image_tag.get("src")
            img_url = self.url_header + image_src.replace("../", "")
            pattern = f"{self.url_header}.+?advanced_information_id=\d+&index=\d+"
            result = re.search(pattern, img_url)
            if result:
                image_url = result.group()
                image_url_list.append(image_url)
        return image_url_list


if __name__ == "__main__":
    pass

# In[ ]:
