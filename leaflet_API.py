import json
import requests
import time
import config
from ScrapingBot import TokubaiBot, YamadaBotCustomTokubai

GOOGLE_URL = config.GOOGLE_URL

class KeepStorage:
    base64_dict = {}

def tokubai_process(stored_hash_list):
    name_list = ["cosmo", "matsumoto", "sugi"]
    shop_id_list = ["115207","44919", "258839"]
    for name, shop_id in zip(name_list, shop_id_list):
        bot = TokubaiBot(name, shop_id)
        bot.get_leaflet_images()
        bot.new_leaflet_post_to_line(stored_hash_list)
        base64_dict = bot.output_update_base64_dictionary()
        KeepStorage.base64_dict.update(base64_dict)

def yamada_process(stored_hash_list):
    bot = YamadaBotCustomTokubai("yamada")
    bot.get_leaflet_images()
    bot.new_leaflet_post_to_line(stored_hash_list)
    base64_dict = bot.output_update_base64_dictionary()
    KeepStorage.base64_dict.update(base64_dict)

def get_stored_leaflet_hash():
    print("get-API...")
    response = requests.get(GOOGLE_URL)
    content = response.json()
    return content

def post_to_leaflet_update(base64_dict):
    print("post-API...")
    data = json.dumps(base64_dict)
    response = requests.post(GOOGLE_URL, data=data)
    print(f"Response Code: {response.status_code} - {response.text}")

def main():
    print("start...")
    start = time.time()
    api_dict = get_stored_leaflet_hash()
    stored_hash_list = api_dict["leaflet_hash"].split(",")

    yamada_process(stored_hash_list)
    tokubai_process(stored_hash_list)

    post_to_leaflet_update(KeepStorage.base64_dict)
    print("...END")
    print(f"PROCCESSING TIME: {round(time.time()-start)} sec")
    return

if __name__ == "__main__":
    main()