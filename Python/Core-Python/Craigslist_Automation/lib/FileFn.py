import os;
import xml.etree.ElementTree as ET;     #XmlReader
import urllib.request as urlParser;
import random;
import re;
class FileFn():
    def destroyfile(file):
        try:
            os.remove(file);
            return True;
        except Exception as err:
            return False;
      
    def makeDirs(dir):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir);
            
            return True;
        except Exception as ex:
            return "Can't Create Directories. Must be path or Permission Issues.";

        
    def readFile(file):
        if not os.path.isfile(file):
            return False;
            
        try:
            handle = open(file, 'rb+');
            ret = handle.read().decode('ascii');
            handle.close()
            if not ret:
                return False;
            
            return ret;

        except Exception as e:
            return False;
            
    def putXml(link, file):
        try:
            print(link);
            string = urlParser.urlopen(link, timeout=25).read();
            tree = ET.ElementTree(ET.fromstring(string));
            fhandle = open(file, 'wb');
            fhandle.write(string);
            fhandle.close();
            return True;
        except Exception as err:
            return err;
    
    def urlTrigger(link):
        try:
            string = urlParser.urlopen(link, timeout=25);
            return True;
        except Exception as err:
            return err;
            
    def getAd(file):
        try:
            rootAd = ET.parse(file).getroot();
            FileFn.destroyfile(file);
            return rootAd;
        except Exception as err:
            return err;
    
    def readProxy(file):
        file = open(file);
        record = random.choice(list(file));
        file.close();
        if record == '':
            return False;
        
        return record.split(":");
     
    def readUseragent(file):
        if not os.path.isfile(file):
            return False;
        
        file = open(file);
        record = random.choice(list(file));
        file.close();
        if record == '':
            return False;
        
        return record;
    
    def checkXmlFormat(file):
        if not os.path.isfile(file):
            return False;
            
        with open(file, 'r') as dfile:
            # Remove tabs, spaces, and new lines when reading
            data = re.sub(r'\s+', '', dfile.read())
            if (re.match(r'^<.+>$', data)):
                return True;
                
            return False;