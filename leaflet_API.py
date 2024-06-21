import json
import requests
import time
import os
from ScrapingBot import TokubaiBot, YamadaBotCustomTokubai

GOOGLE_URL = os.environ.get('LEAFLET_MANAGEMENT_URL')
LINE_NOTIFY_TOKEN = os.environ.get('LINE_NOTIFY_TOKEN')


class KeepStorage:
    base64_dict = {}
    update_flag = False


def tokubai_process(shop_dict, stored_hash_list):
    for name, shop_id in shop_dict.items():
        bot = TokubaiBot(name, shop_id, LINE_NOTIFY_TOKEN)
        bot.get_leaflet_images()
        bot.new_leaflet_post_to_line(stored_hash_list)
        base64_dict = bot.output_base64_dictionary()
        KeepStorage.base64_dict.update(base64_dict)
        if bot.post_flag:
            KeepStorage.update_flag = True


def yamada_process(stored_hash_list):
    bot = YamadaBotCustomTokubai("yamada", LINE_NOTIFY_TOKEN)
    bot.get_leaflet_images()
    bot.new_leaflet_post_to_line(stored_hash_list)
    base64_dict = bot.output_base64_dictionary()
    KeepStorage.base64_dict.update(base64_dict)
    if bot.post_flag:
        KeepStorage.update_flag = True


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
    SHOP_INFOMATION = {"cosmo": "115207",
                       "matsumoto": "44919", "sugi": "258839"}

    api_dict = get_stored_leaflet_hash()
    stored_hash_list = api_dict["leaflet_hash"].split(",")
    yamada_process(stored_hash_list)
    tokubai_process(SHOP_INFOMATION, stored_hash_list)

    if KeepStorage.update_flag:
        post_to_leaflet_update(KeepStorage.base64_dict)
    else:
        print("Update is Nothing")

    print("...END")
    print(f"PROCCESSING TIME: {round(time.time()-start)} sec")
    return


if __name__ == "__main__":
    main()
