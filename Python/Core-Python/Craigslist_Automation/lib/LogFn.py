import os;
import re;
import sys;
import logging
import warnings
import urllib.request as urlParser;
import linecache;   #To catch line Error

from lib.TimeFn import TimeFn;
from lib.FileFn import FileFn;


class LogFn():
    def __init__(self, path, host):
        self.path           = path;
        self.host           = host;
        self.sep            = os.sep;
        
        self.reportsRpDir   = self.path + self.sep + "reports";
        self.replaceRpDir   = self.reportsRpDir + self.sep + "replaces" + self.sep + host;
        self.errorsRpDir    = self.reportsRpDir + self.sep + "errors" + self.sep + host;
        self.dataDir        = self.path + self.sep + "data" + self.sep + host;
        
        FileFn.makeDirs(self.reportsRpDir);
        FileFn.makeDirs(self.replaceRpDir);
        FileFn.makeDirs(self.errorsRpDir);
        FileFn.makeDirs(self.dataDir);
        
        self.logger         = logging.getLogger('LogApp');
        hdlr                = logging.FileHandler(self.errorsRpDir + self.sep + 'log-' + TimeFn.getCurrentDate() + '.txt');
        formatter           = logging.Formatter('%(asctime)s %(levelname)s %(message)s');
        formatter           = logging.Formatter('%(asctime)s %(levelname)s %(message)s');
        
        hdlr.setFormatter(formatter);
        self.logger.addHandler(hdlr);
        
    def logInfo(self, msg):
        print(msg + "\n");
        self.logger.info(msg);
    
    def logErr(self, msg):
        print(msg + "\n");
        self.logger.error(msg);

    def printExp(self):
        try:
            exc_type, exc_obj, tb = sys.exc_info()
            f           = tb.tb_frame
            lineno      = tb.tb_lineno
            filename    = f.f_code.co_filename
            linecache.checkcache(filename)
            line        = linecache.getline(filename, lineno, f.f_globals)
            return 'EXCEPTION IN ({}, LINE {} "{}"): {}' . format(filename, lineno, line.strip(), exc_obj);
        except Exception as ex:
            return "Can't get ERROR in Print Exception function.";
            
    
    def errorTrigger(self, eType=None, err=None, dealer=None, campaign=None):
        try:
            #eeType  = urlParser.pathname2url(re.sub("[:\']", "-", eType));
            #eerr    = urlParser.pathname2url(re.sub("[:\']", "-", err));
            if dealer is None:
                dealer = '';
            
            if campaign is None:
                campaign = '';
            
            #Write Error to URL
            ##print(url);
            #retText = urlRequest.urlopen(url, timeout=10);
            #Write Error to File
            self.logErr(format(eType) + " -- " + format(err) + " -- " + format(self.printExp()));
        except Exception as err:
            print('Error in Writing Logs either to DB or file - ' + format(self.printExp()));
            return False;
