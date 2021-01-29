import configparser;

class configLoader():
     def __init__(self, cfile):
        config = configparser.ConfigParser();
        config.read(cfile);
        self.settings = config['DEFAULT'];
        
        