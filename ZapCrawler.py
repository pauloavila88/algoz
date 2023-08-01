from datetime import datetime as dt
import multiprocessing
import pandas as pd
import requests
import random
import urllib
import copy
import json
import bs4

import sys
import os

LIBRARIES_PATH = '/Users/estoca/PycharmProjects/jupyter/my_python_libraries'
sys.path.insert(0, LIBRARIES_PATH)

import Utils
import Log
import Gsheets
import Credentials

CREDENTIALS_PATH = '/Users/estoca/PycharmProjects/jupyter/credentials/cava_analysis'

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
        self.gs = Gsheets.Gsheet(CREDENTIALS_PATH)
        self.lg = Log.Log()
    
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
            elems = _elem.find_all('div',{'class': 'simple-card__actions'})[0].find_all('ul')[0].find_all('li',{'class':_attr})[0].find_all('span')
            return elems[1].text.replace('\n','').strip() if(len(elems)> 0) else ''
        except Exception as e:
            return ''

        
    def get_link(self,_elem):
        return 'https://www.zapimoveis.com.br/imovel/'+_elem['data-id']

    
    def get_address(self,_elem):
        try:
            return _elem.find_all('h2',{'class': 'simple-card__address'})[0].text 
        except Exception as e:
            return ''

        
    def get_description(self,_elem):
        try:
            res = _elem.find_all('div',{'class':'simple-card__description'})
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
            res = _elem.find_all('p',{'class':'simple-card__price'})
            return res[0].text.strip() if len(res) > 0 else ''
        except Exception as e:
            return ''
        
        
    def get_image(self,_elem):
        try:
            res = _elem.find_all('div',{'class':'carousel__wrapper'})
            return res[0].find('img')['src'] if len(res) > 0 else ''
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
        
        
    ######################
    # Get Input from Sheets
    ######################
    
    
    def get_input(self):
        i = self.gs.get_data(self.SHEET_INFO['input'])
        return i[0]['address'], i[0]['pages'], i[0]['place_type'], i[0]['purchase_type']
    
        
    ######################
    # Parse results
    ######################
    
    
    def get_page_info(self, search_input, _retry=0): 
        url = f"https://www.zapimoveis.com.br/{search_input['purchase_type']}/{search_input['place_type']}/{search_input['address']}?pagina={search_input['page']}&ordem=Valor&transacao=Venda"

        # Get Data from URL
        res = requests.get(url, headers=self.headers, timeout=7)
        return res
    
    
    def parse_res(self, _res, _search_input, _retry=0):
        partial_listings = []
        
        if not _res:
            self.log(f"res is None for page {_page}")
        else:
            soup = bs4.BeautifulSoup(_res.text)
        
            # Get Data
            card_containers = soup.find_all('div',{'class': 'card-container'})
            self.log(f'Total find: {len(card_containers)}',2)

            for card in card_containers:
                partial_listings.append({
                     'timestamp': _search_input['timestamp']
                    ,'link': self.get_link(card)
                    ,'area': self.get_attr(card,'js-areas')
                    ,'bedrooms': self.get_attr(card,'js-bedrooms')
                    ,'parking': self.get_attr(card,'js-parking-spaces')
                    ,'bathrooms': self.get_attr(card,'js-bathrooms')
                    ,'address': self.get_address(card).strip()
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
                if len(data)  == 0:
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

        status += self.log_results(t0, address, final_page, len(listings), status)
        
        return status
    

def main():
    zn = ZapCrawler(_debug=True) #, _parallel=False)
    zn.execute()

if __name__ == "__main__":
    main()