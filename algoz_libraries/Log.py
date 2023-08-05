from . import Utils

import datetime as dt

class Log:
    MSG_LIMIT = 1000
    def __init__(self,_filename=''):
        if(len(_filename) > 0):
            self.persist = True
            self.filename = _filename
        else:
            self.persist = False

        self.utils = Utils.Utils()
        
    def time_val(self,_start):
        seconds = (dt.datetime.now() - _start).total_seconds()
        
        if(seconds > 3600):
            return '%s%s'%(round(seconds/3600,2),'h')
        
        if(seconds > 60):
            return '%s%s'%(round(seconds/60,2),'m')
        
        if(seconds < 60):
            return '%s%s'%(round(seconds,2),'s')
            
    def log(self,_msg,_indent=0,_t0=None):
        time_taken = ''
        if(_t0):
            time_taken = ' >> Time taken: %s'%self.time_val(_t0)
        msg = '%s:%s %s%s'%(self.utils.get_datestr(),'   '*_indent,_msg,time_taken)
        print(msg[:Log.MSG_LIMIT])
        if(self.persist):
            with open(self.filename, 'a') as f:
                f.write(msg+'\n')