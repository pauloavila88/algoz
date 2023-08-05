import datetime as dt
import xlsxwriter
import random
import uuid
import time
import csv
import os
import re

class Utils:
    def wait(self,_time=2,_rand=True):
        """Sleep for a set time. By defaul will sleep betwen a random time between the time and it's double."""
        stop = random.randrange(_time*100,_time*100*2)/100 if _rand else _time
        time.sleep(stop)
    
    def check_keys(self,_dict,_keys_to_check=[]):
        """Check if a whole list of keys is inside a dict. Also checks if any list inside a matrix is inside a dict"""
        if len(_keys_to_check) == 0:
            return False
        else:
            if(all(isinstance(n, list) for n in _keys_to_check)):
                checks = [True if all ( k in _dict for k in check) else False for check in _keys_to_check]
            else:
                checks = [True if all ( k in _dict for k in _keys_to_check) else False]
            return True if sum(checks) > 0 else False
    
    def extract_regex(self,_text,_regex):
        """Extract the text from regex"""
        find_val = re.search(_regex,_text,re.IGNORECASE)
        return find_val.group(1) if find_val else ''
    
    def encode_val(self,_val):
        """Encode the values tos utf-8"""
        return _val.encode('utf-8') if type(_val) in [str] else str(_val).encode('utf-8')
        
    def get_datestr(self):
        """Return the current datetime formatted"""
        now = dt.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')
    
    def list_files(self,_path):
        """List all files inside a folder"""
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(_path):
            for file in f:
                files.append(os.path.join(r, file))

        return files
    
    def replace_params(self,_string,_params):
        """Replace every {{key}} with the value"""
        for k in _params:
            _string = _string.replace('{{%s}}'%k,str(_params[k]))
            
        return _string

    def csv_to_excel(self,_csv_path):
        """Transform CSV to XLSX File"""
        t0 = dt.datetime.now()
        file_name = _csv_path[_csv_path.rfind('/'):] if _csv_path.find('/') > 0 else _csv_path
        file_name = file_name if file_name.find('.') > 0 else file_name+'.csv'
        
        wb = xlsxwriter.Workbook(file_name.replace(".csv",".xlsx"))
        ws = wb.add_worksheet(file_name[:-4])    # your worksheet title here

        lg.log('Reading CSV...',2)
        with open(file_name,'r') as csvf:
            table = csv.reader(csvf,quotechar='"', delimiter=',',
                             quoting=csv.QUOTE_ALL, skipinitialspace=True)

            i = 0
            # write each row from the csv file as text into the excel file
            # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
            total_size = 1104792

            for idx,row in enumerate(table):
                ws.write_row(i, 0, row)
                i += 1
        lg.log('Saved csv %s to file %s!'%(_csv_path,file_name) ,2,t0)
        wb.close()
        
        import random
        
    def uuid(self):
        return str(uuid.uuid1())

    def short_uid(self,_size=8):
        uid_chars = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0')

        count=len(uid_chars)-1
        c=''
        for i in range(0,_size):
            c+=uid_chars[random.randint(0,count)]
        return c