from datetime import datetime as dt
import multiprocessing
import pandas as pd
import requests
import random
import urllib
import copy
import json
import bs4
import os
import time

from .algoz_libraries import Utils
from .algoz_libraries import Log
from .algoz_libraries import Gsheets

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
CREDENTIAL_DIR = os.path.join(CURRENT_PATH, "confidential")

LISTINGS_API_MAX_SIZE = 110
LOCATAIONS_PER_TYPE_HTML = 10

class ZapCrawler():
    SHEET_LINK = 'https://docs.google.com/spreadsheets/d/1STby0O8UVFf4eogehMQVMKPRZnniLBQLF6-ZmXSUjMo/edit#gid=0'
    SHEET_INFO = {
         'data':{
             'url': SHEET_LINK
            ,'tab': 'data'
        }
        ,'input':{
             'url': SHEET_LINK
            ,'tab': 'input'
        }
        ,'log':{
             'url': SHEET_LINK
            ,'tab': 'log'
        }
        ,'debug_log':{
             'url': SHEET_LINK
            ,'tab': 'debug_log'
        }
    }
    
    MAX_RETRIES = 5
    FORCE_PROXY_UPDATE = False
    
    USER_AGENT_LIST = [
                # Chrome
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                'Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Mozilla/5.0 (en-us) AppleWebKit/534.14 (KHTML, like Gecko; Google Wireless Transcoder) Chrome/9.0.597 Safari/534.14 wimb_monitor.py/1.0',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',

                # Safari
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
                'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1',
                'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
                'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; de-de) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            ]
    
        
    def __init__(self, _debug=False):
        self.gs = Gsheets.Gsheet(CREDENTIAL_DIR)
        self.lg = Log.Log()
        self.utils = Utils.Utils()

        self.headers = {'User-Agent': random.choice(self.USER_AGENT_LIST) }
        self.proxy = None
        self.debug = _debug
        

    def log(self, msg, indent=None, _time=None):
        if self.debug:
            self.lg.log(msg, indent, _time)
        
            
    ######################
    # Get information
    ######################
            
        
    def get_attr(self,_elem,_attr):
        try:
            elems = _elem.find_all('p',{'class': 'card__amenity', 'itemprop': _attr}) if _attr != None\
                    else _elem.find_all('p',{'class': 'card__amenity'}, itemprop=None)       # Upwork - Vargas update (The website html have changed)
            return elems[0].text.replace('\n','').strip() if(len(elems)> 0) else ''          # Upwork - Vargas update (The website html have changed)
        except Exception as e:
            return ''

    def get_link(self,_elem):
        return 'https://www.zapimoveis.com.br/imovel/'+_elem['data-id']

    def get_address(self,_elem):
        try:
            return f"{_elem.find_all('h2',{'class': 'card__address'})[0].text.strip()} - {_elem.find_all('p',{'class': 'card__street'})[0].text.strip()}"  # Upwork - Vargas update (The website html have changed)
        except Exception as e:
            return ''

    def get_description(self,_elem):
        try:
            res = _elem.find_all('p',{'class':'card__description'})     # Upwork - Vargas update (The website html have changed)
            return res[0].text if len(res) > 0 else ''
        except Exception as e:
            return ''

    def get_tag(self,_elem):
        try:
            res = _elem.find_all('div',{'class':'badge'})
            return res[0].text if len(res) > 0 else ''
        except Exception as e:
            return ''
        
    def get_price(self,_elem):
        try:
            res = _elem.find_all('div',{'class':'listing-price'})[0].find_all('p')      # Upwork - Vargas update (The website html have changed)
            return res[0].text.strip() if len(res) > 0 else ''
        except Exception as e:
            return ''
        
    def get_image(self,_elem):
        try:
            res = _elem.find_all('ul',{'class':'l-carousel-image__list'})[0].find_all('img')        # Upwork - Vargas update (The website html have changed)
            images = []
            for image in res:                                                                       # Upwork - Vargas update (Save all images instead of first only)
                images.append(image['src'])
            return json.dumps(images) if len(images) > 0 else ''
        except Exception as e:
            return ''
    
    
    ######################
    # Save information
    ######################
        
        
    def save_res(self,_res):
        self.gs.save(self.SHEET_INFO['data']
                ,pd.DataFrame(_res).astype(str)
                ,_cols=['timestamp','address','area','bedrooms','parking'
                        ,'bathrooms','tag','description','price','image','link'])
        
    def create_res(self, _name, _res, _share_users):
        return self.gs.create(
            _name,
            pd.DataFrame(_res).astype(str),
            _cols=['timestamp','tag','address','area','bedrooms','parking','bathrooms','description','price','image','link'], 
            _share_users = _share_users
        )
        
        
    ######################
    # Get Input from Sheets
    ######################
    
    
    def get_input(self):
        i = self.gs.get_data(self.SHEET_INFO['input'])
        return i[0]['address'], i[0]['pages'], i[0]['place_type'], i[0]['purchase_type']
    
        
    ######################
    # Parse results - Front-End
    ######################
    
    
    def get_page_info(self, search_input, _retry=0): 
        # url = f"https://www.zapimoveis.com.br/{search_input['purchase_type']}/{search_input['place_type']}/{search_input['address']}?pagina={search_input['page']}&ordem=Valor&transacao=Venda"
        url = f"https://www.zapimoveis.com.br/{search_input['purchase_type']}/{search_input['place_type']}/{search_input['address']}?pagina={search_input['page']}&ordem=Menor%20preço&transacao=venda"     # Upwork - Vargas update (ordem=Valor > ordem=Menor%20preço)

        # Get Data from URL
        res = requests.get(url, headers=self.headers, timeout=7)
        return res
    
    def parse_res(self, _res, _search_input, _retry=0):
        partial_listings = []
        
        if not _res:
            self.log(f"res is None for page {_search_input}")                       # Upwork - Vargas update (_page > _search_input)
        else:
            soup = bs4.BeautifulSoup(_res.text, features="html.parser")
            
            # Get Data
            card_containers = soup.find_all('a',{'class': 'result-card'})           # Upwork - Vargas update (The website html have changed)
            self.log(f'Total find: {len(card_containers)}',2)

            for card in card_containers:
                partial_listings.append({
                     'timestamp': _search_input['timestamp']
                    ,'link': self.get_link(card)
                    ,'area': self.get_attr(card,'floorSize')                        # Upwork - Vargas update (The website html have changed)
                    ,'bedrooms': self.get_attr(card,'numberOfRooms')                # Upwork - Vargas update (The website html have changed)
                    ,'parking': self.get_attr(card,None)                            # Upwork - Vargas update (The website html have changed)
                    ,'bathrooms': self.get_attr(card, 'numberOfBathroomsTotal')     # Upwork - Vargas update (The website html have changed)
                    ,'address': self.get_address(card)                              # Upwork - Vargas update (The website html have changed)
                    ,'tag': self.get_tag(card)
                    ,'description': self.get_description(card)
                    ,'price': self.get_price(card)
                    ,'image': self.get_image(card)
                })
        
        return partial_listings
    
    def parse_page(self, search_input, _retry=0):
        self.log(f"Running for page {search_input['page']}...",2)

        res = self.get_page_info(search_input, _retry)
        _partial_listings = self.parse_res(res, search_input, _retry)
        
        return _partial_listings
    
    
    ######################
    # Parse results - Back-End
    ######################


    # > LOCATIONS
    def request_locations(self, search_input, _size="10", _retry=0): 
        api_url = "https://glue-api.zapimoveis.com.br/v3/locations"
        params = {
            "q": search_input['query'],
            "businessType": search_input['businessType'],
            "listingType": search_input['listingType'],
            "constructionStatus": search_input['constructionStatus'],
            "size": _size,
            "portal": "ZAP",
            "amenities": "Amenity_NONE",
            "fields": "neighborhood,city,street,condominium,account,poi",   #
            "includeFields": "address.neighborhood,address.city,address.state,address.zone,address.locationId,address.point,url,advertiser.name,uriCategory.page,condominium.name,address.street",
            "__zt": "mtc:deduplication",
            "unitTypes": ""
        }

        # Request Data
        for _ in range(_retry if _retry>0 else 1):
            res = requests.request("GET", api_url, headers=self.headers, params=params)
            if res.status_code == 200:
                break
            self.utils.wait(_time=0.5, _rand=True)
        return res.json()

    def parse_locations(self, locations_input):
        translations = {
            "street": "Ruas",
            "neighborhood": "Bairros",
            "city": "Cidades"
        }
        locations_output = {
            "Cidades": None,
            "Bairros": None,
            "Ruas": None
        }
        for k, v in locations_input.items():
            if k not in translations:
                continue
            count_locations = len(v["result"]["locations"])
            out_main_key = translations[k]
            locations_output[out_main_key] = {}
            locations_output[out_main_key]["totalCount"] = v["totalCount"]
            if count_locations > 0:
                locations_output[out_main_key]["locations"] = {}
                for count, location in enumerate(v["result"]["locations"]):
                    location_id = f"{out_main_key}-{count}"
                    locations_output[out_main_key]["locations"][location_id] = location

                    state_initials = ""
                    for state_name in location['address']['state'].split(" "):
                        state_initials += state_name.strip()[0] if state_name.strip()[0].isupper() else ""

                    if k == "city":
                        description = f'{location["address"]["city"]} - {state_initials}'
                    elif k == "neighborhood":
                        description = f'{location["address"]["neighborhood"]}, {location["address"]["city"]} - {state_initials}'
                    elif k == "street":
                        description = f'{location["address"]["street"]}, {location["address"]["city"]} - {state_initials}'
                    else:
                        continue

                    locations_output[out_main_key]["locations"][location_id]["description"] = description

            else:
                locations_output[out_main_key]["locations"] = {}

        return locations_output
            
    def get_locations(self, search_input, _size=LOCATAIONS_PER_TYPE_HTML, _retry=0):
        try:
            loc_req = self.request_locations(search_input, _size, _retry)
            if "err" in loc_req:
                return loc_req
            return self.parse_locations(loc_req)
        except Exception as e:
            return {"err": e}


    # > LISTINGS
    def request_listings(self, search_input, _size="0", _page="1", _from="0", _retry=0):
        utils = Utils.Utils()
        api_url = "https://glue-api.zapimoveis.com.br/v2/listings"
        
        params = {
            "categoryPage":search_input['categoryPage'],
            "business":search_input['businessType'],
            "listingType":search_input['listingType'],
            "constructionStatus":search_input['constructionStatus'],
            "addressType":search_input['addressType'],
            "addressStreet":search_input['addressStreet'],
            "addressNeighborhood":search_input['addressNeighborhood'],
            "addressZone":search_input['addressZone'],
            "addressCity":search_input['addressCity'],
            "addressState":search_input['addressState'],
            "addressLocationId":search_input['addressLocationId'],
            "addressPointLat":search_input['addressPointLat'],
            "addressPointLon":search_input['addressPointLon'],
            "size":_size,
            "page":_page,
            "from":_from,
            # "__zt": "mtc:deduplication",
            "includeFields":"search(result(listings(listing(listingsCount,sourceId,displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status,priceSuggestion,contractType),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,createdDate,minisite,tier),medias,accountLink,link)),totalCount),page,facets,fullUriFragments,developments(search(result(listings(listing(listingsCount,sourceId,displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status,priceSuggestion,contractType),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,createdDate,minisite,tier),medias,accountLink,link)),totalCount))",
        }
        if search_input['unit_type'] != {}:
            for k,v in search_input['unit_type'].items():
                params[k] = v

        if "sort" in search_input:
            params["sort"] = search_input["sort"]
        
        print("Incoming Request:", json.dumps(params, indent=2))

        headers=self.headers
        headers["x-domain"] = "www.zapimoveis.com.br"

        # Request Data
        for _ in range(_retry if _retry>0 else 1):
            res = requests.request("GET", api_url, headers=self.headers, params=params)
            if res.status_code == 200:
                # print(f"[ DEBUG ] -> Listing Request:\Response={json.dumps(res.json(), indent=2)}")
                break
            utils.wait(_time=0.7, _rand=True)

        return res.json()
    
    def parse_listings_totalCount(self, listings_input):
        return {
            # "listings": listings_input["search"]["result"]["listings"] if self.utils.keys_exists(listings_input, 'search', 'result', 'listings') else ',   # Since _size=0 listings will be an empty array [] -> No need to return it
            "amenities": listings_input["facets"]["amenities"] if self.utils.keys_exists(listings_input, 'facets', 'amenities') else '',
            "totalCount": listings_input["search"]["totalCount"] if self.utils.keys_exists(listings_input, 'search', 'totalCount') else ''
        }
    
    def parse_link(self, href):
        return f'https://www.zapimoveis.com.br{href}'

    def parse_image_link(self, link, _image_description='zapcrawler'):
        _image_width = '614'
        _image_height = '297'
        replace_tags = {
            '{action}': 'crop',
            '{width}': _image_width,
            '{height}': _image_height,
            '{description}': _image_description
        }
        out_link = link
        
        for k, v in replace_tags.items():
            out_link = out_link.replace(k, v)

        return out_link

    def parse_listing_address(self, listing):
        _adress = ""
        # Door Number
        _adress += f"{listing['listing']['address']['streetNumber']}" if self.utils.keys_exists(listing, 'listing', 'address', 'streetNumber') and listing['listing']['address']['streetNumber'] != "" else ''     
        # Street
        _adress += f" {listing['listing']['address']['street']}" if self.utils.keys_exists(listing, 'listing', 'address', 'street') and listing['listing']['address']['street'] != "" else ''                
        # Neighborhood
        _adress += f" - {listing['listing']['address']['neighborhood']}" if self.utils.keys_exists(listing, 'listing', 'address', 'neighborhood') and listing['listing']['address']['neighborhood'] != "" else ''    
        # City
        _adress += f", {listing['listing']['address']['city']}" if self.utils.keys_exists(listing, 'listing', 'address', 'city') and listing['listing']['address']['city'] != "" else '' 
        # State
        _adress += f" - {listing['listing']['address']['state']}" if self.utils.keys_exists(listing, 'listing', 'address', 'state') and listing['listing']['address']['state'] != "" else ''
        # Zip Code
        _adress += f", {listing['listing']['address']['zipCode'][:5]}-{listing['listing']['address']['zipCode'][5:]}" if self.utils.keys_exists(listing, 'listing', 'address', 'zipCode') and listing['listing']['address']['zipCode'] != "" and len(listing['listing']['address']['zipCode']) == 8 else ''                
        # Zone
        # _adress += f"{listing['listing']['address']['zone']}, " if self.utils.keys_exists(listing, 'listing', 'address', 'zone') and listing['listing']['address']['zone'] != "" else ''               
        # District
        # _adress += f"{listing['listing']['address']['district']}, " if self.utils.keys_exists(listing, 'listing', 'address', 'district') and listing['listing']['address']['district'] != "" else ''                                    
        # Country
        # _adress += f"{listing['listing']['address']['country']} " if self.utils.keys_exists(listing, 'listing', 'address', 'country') and listing['listing']['address']['country'] != "" else ''               
        return _adress

    def parse_listing_price(self, priceInfos, businessType):
        for priceInfo in priceInfos:
            if priceInfo['businessType'] == businessType:
                return priceInfo['price']
        return ''

    def parse_listings_possibilities(self, listings_input):
        partial_listings = []
        listings = listings_input["search"]["result"]["listings"]
        for listing in listings:
            partial_listings.append({
                'timestamp': dt.now(),
                'link': self.parse_link(listing['link']['href']) if self.utils.keys_exists(listing, 'link', 'href') else '',
                'id': listing['listing']['id'] if self.utils.keys_exists(listing, 'listing', 'id') else '',
                'area': listing['listing']['usableAreas'] if self.utils.keys_exists(listing, 'listing', 'usableAreas') else '',
                'bedrooms': listing['listing']['bedrooms'] if self.utils.keys_exists(listing, 'listing', 'bedrooms') else '',
                'parking': listing['listing']['parkingSpaces'] if self.utils.keys_exists(listing, 'listing', 'parkingSpaces') else '',
                'bathrooms': listing['listing']['bathrooms'] if self.utils.keys_exists(listing, 'listing', 'bathrooms') else '',
                'tag': listing['link']['name'] if self.utils.keys_exists(listing, 'link', 'name') else '',
                'description': listing['listing']['description'] if self.utils.keys_exists(listing, 'listing', 'description') else '',
                'price': listing['listing']['pricingInfos'][0]['price'] if self.utils.keys_exists(listing, 'listing', 'pricingInfos', 0, 'price') else '',
                'image': [ self.parse_image_link(value['url']) for value in listing['medias'] if self.utils.keys_exists(value, 'url') and  self.utils.keys_exists(value, 'type') and value['type'] == 'IMAGE'] ,    # TODO `keys_exists`
                'address': {
                    'locationId': listing['listing']['address']['locationId'] if self.utils.keys_exists(listing, 'listing', 'address', 'locationId') else '',
                    'country':listing['listing']['address']['country'] if self.utils.keys_exists(listing, 'listing', 'address', 'country') else '',
                    'state':listing['listing']['address']['state'] if self.utils.keys_exists(listing, 'listing', 'address', 'state') else '',
                    'stateAcronym':listing['listing']['address']['stateAcronym'] if self.utils.keys_exists(listing, 'listing', 'address', 'stateAcronym') else '',
                    'district':listing['listing']['address']['district'] if self.utils.keys_exists(listing, 'listing', 'address', 'district') else '',
                    'city':listing['listing']['address']['city'] if self.utils.keys_exists(listing, 'listing', 'address', 'city') else '',
                    'zone':listing['listing']['address']['zone'] if self.utils.keys_exists(listing, 'listing', 'address', 'zone') else '',
                    'neighborhood':listing['listing']['address']['neighborhood'] if self.utils.keys_exists(listing, 'listing', 'address', 'neighborhood') else '',
                    'street':listing['listing']['address']['street'] if self.utils.keys_exists(listing, 'listing', 'address', 'street') else '',
                    'streetNumber':listing['listing']['address']['streetNumber'] if self.utils.keys_exists(listing, 'listing', 'address', 'streetNumber') else '',
                    'zipCode':listing['listing']['address']['zipCode'] if self.utils.keys_exists(listing, 'listing', 'address', 'zipCode') else '',
                },
                'advertiser':{
                    'name':listing['account']['name'] if self.utils.keys_exists(listing, 'account', 'name') else '',
                    'accountLink':listing['accountLink']['href'] if self.utils.keys_exists(listing, 'accountLink', 'href') else '',
                    'advertiserId':listing['account']['id'] if self.utils.keys_exists(listing, 'account', 'id') else '',
                    'contacts':listing['listing']['advertiserContact']['phones'] if self.utils.keys_exists(listing, 'listing', 'advertiserContact', 'phones') else '',
                    'whatsappNumber':listing['listing']['whatsappNumber' if self.utils.keys_exists(listing, 'listing', 'whatsappNumber') else '']
                }
            })
        # print(json.dumps({'debug':partial_listings}, indent=2))
        
        return  partial_listings

    def parse_listings(self, listings_input, businessType):
        partial_listings = []
        listings = listings_input["search"]["result"]["listings"]
        for listing in listings:
            _parsed_listing = {
                    'timestamp': dt.now(),
                    'address': self.parse_listing_address(listing),
                    'area': listing['listing']['usableAreas'][0] if self.utils.keys_exists(listing, 'listing', 'usableAreas') and len(listing['listing']['usableAreas'])>0 else '',
                    'bedrooms': listing['listing']['bedrooms'][0] if self.utils.keys_exists(listing, 'listing', 'bedrooms') and len(listing['listing']['bedrooms'])>0 else '',
                    'parking': listing['listing']['parkingSpaces'][0] if self.utils.keys_exists(listing, 'listing', 'parkingSpaces') and len(listing['listing']['parkingSpaces'])>0 else '',
                    'bathrooms': listing['listing']['bathrooms'][0] if self.utils.keys_exists(listing, 'listing', 'bathrooms') and len(listing['listing']['bathrooms'])>0 else '',
                    'tag': listing['link']['name'] if self.utils.keys_exists(listing, 'link', 'name') else '',
                    'description': listing['listing']['description'] if self.utils.keys_exists(listing, 'listing', 'description') else '',
                    'price': self.parse_listing_price(listing['listing']['pricingInfos'], businessType) if self.utils.keys_exists(listing, 'listing', 'pricingInfos') and len(listing['listing']['pricingInfos'])>0 else '',
                    'image': json.dumps([ self.parse_image_link(value['url']) for value in listing['medias'] if self.utils.keys_exists(value, 'url') and  self.utils.keys_exists(value, 'type') and value['type'] == 'IMAGE']) ,
                    'link': self.parse_link(listing['link']['href']) if self.utils.keys_exists(listing, 'link', 'href') else ''
                }
            
            partial_listings.append(_parsed_listing)
            
        return  partial_listings

    def get_listings(self, search_input, _retry=0):
        try:
            # Retrieve totalCount of Listings
            if search_input['ammount'] == '0':
                lis_req = self.request_listings(search_input, _retry=_retry)
                if "err" in lis_req:
                    return lis_req
                return self.parse_listings_totalCount(lis_req)
            
            # Spreadsheet Construction with Listings
            _ammount = int(search_input['ammount'])
            _page_counter=1
            _from = 0
            _ammount_counter = 0
            listings = []
            _pages_retry=self.MAX_RETRIES
            while True:
                size = LISTINGS_API_MAX_SIZE if _ammount - _from  > LISTINGS_API_MAX_SIZE else _ammount - _from
                lis_req = self.request_listings(search_input, _size=str(size), _page=str(_page_counter), _from=str(_from), _retry=_retry)
                self.utils.wait(_time=0.5, _rand=True)
                if "err" in lis_req:
                    return lis_req
                
                parsed_listings = self.parse_listings(lis_req, search_input['businessType'])
                
                if len(parsed_listings) == 0:
                    _page_counter += 1
                    _pages_retry -= 1
                    if _pages_retry <= 0:
                        break
                    continue

                listings += parsed_listings

                _from += len(parsed_listings)
                _ammount_counter += len(parsed_listings)
                if _ammount_counter >= _ammount:
                    break
            
            # Create GSheet with results
            gsheet_url = self.create_res(search_input['sheet_name'], listings, search_input['sheet_share_users'])

            return{"listings": listings, 'gsheet_url': gsheet_url}
        
            # self.log(f'Finished! Total results {len(listings)}...', 3, dt.now())
        except Exception as e:
            return {"err": e}


    ######################
    # Log Results
    ######################
    
    
    def log_results(self, _t0, _address, _final_page, _total_listings, _status):
        sts = ''
        try:
            # Log Result
            log = pd.DataFrame([{'timestamp': _t0,
                                 'address': _address,
                                 'pages': _final_page,
                                 'results': _total_listings,
                                 'status': _status}]).astype(str)
            self.gs.save(self.SHEET_INFO['log'],log,_append=True)
        except Exception as e:
            sts += f' > Error on saving result: {e}'
            
        return sts
    
    def log_debug_results(self, _t0, _address, _final_page, _total_listings, _status):
        sts = ''
        try:
            # Log Result
            log = pd.DataFrame([{'timestamp': _t0,
                                 'address': _address,
                                 'pages': _final_page,
                                 'results': _total_listings,
                                 'status': _status}]).astype(str)
            self.gs.save(self.SHEET_INFO['debug_log'],log,_append=True)
        except Exception as e:
            sts += f' > Error on saving result: {e}'
            
        return sts
        
        
    def execute(self):
        listings = []
        parsed_results = []
        t0 = dt.now()
        
        status = ''
        
        try:    
            address, final_page, place_type, purchase_type = self.get_input()
            pages = range(1,final_page+1)

            search_input = []
            for page in pages:
                search_input.append({
                        'address': address,
                        'final_page': final_page,
                        'place_type': place_type,
                        'purchase_type': purchase_type,
                        'page': page,
                        'timestamp': t0
                    })
                
            for i in search_input:
                data = self.parse_page(i)
                if len(data) == 0:
                    break
                else:
                    listings += data
                
            self.log(f'Finished! Total results {len(listings)}...', 3, t0)

            # Save results
            self.save_res(listings)

            status = f'Success, Baroz! Total results {len(listings)}'
        except Exception as e:
            status = f'Error on executing: {e}'
            self.log(status)

        # address|pages|results|status|timestamp
        # status += self.log_results(address, final_page, len(listings), status, t0)
        status += self.log_debug_results(address, final_page, len(listings), status, t0)
        
        return status