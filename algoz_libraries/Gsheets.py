from . import Utils
from . import Log

import pandas as pd
import pygsheets
import string        

class Gsheet:
    
    def __init__(self,_auth_file=''):
        self.gs = pygsheets.authorize(credentials_directory=_auth_file)
        self.utils = Utils.Utils()
        self.log = Log.Log()
    
    ########################
    # Utils
    def colnum_2_colletter(self,_n):
        """From column number, returns column letter"""
        s = ""
        while _n > 0:
            _n, remainder = divmod(_n - 1, 26)
            s = chr(65 + remainder) + s
        return s
    
    def colletter_2_colnum(self,_c):
        """From column letter, returns column number"""
        num = 0
        for c in _c:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num
    
    def resize_sheet(self,_tab,_data,_crange):
        """Add columns and rows if needed"""
        if len(_data) > 0:
            start_col,end_col,start_row, end_row = self.get_data_crange(_data,_crange.split(':')[0])
        
            sheet_cols = _tab.cols 
            start_col = self.colletter_2_colnum(start_col)
            needed_cols = len(_data[0]) + start_col -1
            resize_cols = needed_cols - sheet_cols
            if resize_cols > 0:
                self.log.log('Adding %s cols...'%resize_cols,3)
                _tab.add_cols(resize_cols)
                
            
            sheet_rows = _tab.rows
            needed_rows = len(_data) + start_row - 1
            resize_rows = needed_rows - sheet_rows
            
            if resize_rows > 0:
                self.log.log('Adding %s rows...'%resize_rows,3)
                _tab.add_rows(resize_rows)
                
    def get_data_crange(self,_data,_start_range='A1'):
        """Return the cell range based on a start range and a matrix"""
        start_col = self.utils.extract_regex(_start_range,'(\D+)')
        data_cols = len(_data[0]) + self.colletter_2_colnum(start_col) - 1
        end_col = self.colnum_2_colletter(data_cols)

        start_row = int(self.utils.extract_regex(_start_range,'(\d+)'))
        end_row = len(_data) + start_row 
        
        return start_col,end_col,start_row, end_row
    
    def remove_titles(self,_data,_start_range,_last_data_row):
        """Remove the titles if it's a append"""
        start_col,end_col,start_row, end_row = self.get_data_crange(_data,_start_range)
        return _data[1:] if(start_row < _last_data_row) else _data
        
    def get_last_data_row(self,_tab,_start_range='A1',_data=[]):
        """Identifies the last empty row"""
        start_col,end_col,start_row, end_row = self.get_data_crange(_data,_start_range)
    
        # if trying to paste in a col that doesn't exists yet
        if(self.colletter_2_colnum(end_col) > _tab.cols):
            return 0
        else:
            final_range = '%s%s'%(end_col, _tab.rows)
            rows = _tab.get_values(_start_range,final_range,include_tailing_empty_rows=True)
            max_row =  -1
            for idx,row in enumerate(rows):
                if(len(''.join(row)) == 0): # When all the columns are empty
                    max_row = start_row + idx
                    break

            max_row = (_tab.rows +1) if max_row == -1 else max_row
            return max_row
    
    def parse_gsheet_data(self,_data,_cols,_start_range='A1'):
        """Parse data to add to a google sheet"""
        if type(_data) == pd.core.frame.DataFrame:
            df = _data
        else:
            df = pd.DataFrame(_data[1:],columns=_data[0])
        rows_data = df[_cols].values.tolist() if len(_cols) > 0 else df.values.tolist()
        titles = [_cols] if len(_cols) > 0 else [df.columns.tolist()]
        data = titles + rows_data
        
        return data        
            
    def get_crange(self,_data,_start_range='A1',_last_data_row=0,_is_append=False,_clear=False):
        """Return the correct Cell Range to update based on a data set"""
        start_col,end_col,start_row, end_row = self.get_data_crange(_data,_start_range)
                
        if(_is_append):
            start_row = _last_data_row if start_row < _last_data_row else start_row
            end_row = len(_data) + start_row - 1
            
        return '%s%s'%(start_col,start_row) if _clear else '%s%s:%s%s'%(start_col,start_row,end_col,end_row)

    def check_sheet_info(self,_sheet_info):
        """Check if the sheet info is correct"""
        res = {}
        # Check keys
        necessary_keys = [['id','tab'],['url','tab']]
        if not self.utils.check_keys(_sheet_info,necessary_keys):
            raise KeyError('Sheet Info need tab, start_range and, at least, id or url')
        else:
            # Define 
            if 'id' in _sheet_info:
                res['sheet_id'] = _sheet_info['id']
                res['sheet_url'] = ''
            else:
                res['sheet_url'] = _sheet_info['url']
                res['sheet_id'] = self.utils.extract_regex(_sheet_info['url'],'https://docs.google.com/spreadsheets/d/(.*)/edit')
                
            res['start_range'] = _sheet_info['start_range'] if 'start_range' in _sheet_info else 'A1'
            res['tab_name'] = _sheet_info['tab']            
            
        return res

    ########################
    # Execution
    def get_sheet_info(self,_sheet_info):
        """Get all the sheet info from the object"""
        sheet_info = self.check_sheet_info(_sheet_info) 
        sheet = self.gs.open_by_key(sheet_info['sheet_id'])
        tab = sheet.worksheet_by_title(sheet_info['tab_name'])
        start_range = sheet_info['start_range']
        
        return sheet, tab, start_range
    
    def get_data(self,_raw_sheet_info,return_as_dict=True):
        """Return all data from a sheet_info"""
        sheet, tab, start_range = self.get_sheet_info(_raw_sheet_info)
        self.log.log('Getting all data from sheet %s tab %s...'%(sheet.title,tab.title),2)
        if(return_as_dict):
            return tab.get_all_records()
        else:
            return tab.get_all_values()

    def clear(self,_data,_crange,_tab):
        """Clear data from the sheet"""
        ranges = _crange.split(':')
        start = ranges[0]
        end = '%s%s'%(self.utils.extract_regex(ranges[1],'(\D+)'),_tab.rows)
        self.log.log('Clearing range %s:%s...'%(start,end),2)
        _tab.clear(start,end)
        
        
    def save(self,_raw_sheet_info,_data,_cols=[],_append=False):
        """Save data to a sheet_info"""
        if(len(_data) > 0):
            sheet, tab, start_range = self.get_sheet_info(_raw_sheet_info)
            
            # Parse Data
            data = self.parse_gsheet_data(_data,_cols,start_range)
            last_data_row = self.get_last_data_row(tab,start_range,data) if _append else 0
            data = self.remove_titles(data,start_range,last_data_row) if _append else data
        
            # Get Cell Range
            crange = self.get_crange(data,start_range,last_data_row,_append)
            
            if(not _append):
                self.clear(data,crange,tab)
        
            self.resize_sheet(tab,data,crange)

            self.log.log('Updating tab "%s" on range %s...'%(tab.title,crange),2)
            tab.update_values(crange,data)
            
            return crange