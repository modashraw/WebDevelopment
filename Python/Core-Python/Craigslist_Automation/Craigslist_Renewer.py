#!/usr/bin/python3
__author__ = "Ashish Rawat"
__copyright__ = "Copyright 2016, The Craigslist Project"
__version__ = "1.0.1"
__maintainer__ = "Ashish Rawat"
__email__ = "ashish.rawat417@gmail.com"
__status__ = "Production"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.action_chains import ActionChains;
from selenium.common.exceptions import NoSuchElementException, TimeoutException;

import unittest
import time
import imaplib
import email

#import psutil
import csv
import re
import os
import sys
import subprocess
import urllib.request as urlParser;
import random;
import shutil;
import html.parser;
import xml.etree.ElementTree as ET;     #xml Reader

from lib.BrowserFn import BrowserFn;
from lib.TimeFn import TimeFn;
from lib.LogFn import LogFn;
from lib.FileFn import FileFn;

class Craigist_Renewer(unittest.TestCase):
    hosttype    = "proauto";
    jobtype     = "sold";
    
    def setUp(self):
        self.path           = os.path.abspath(os.path.dirname(sys.argv[0]));
        self.imagesPath     = "/mnt/feed";
        self.clUrl          = "https://accounts.craigslist.org";
        self.sep            = os.sep;
        self.browser        = None;
        
        self.params         = {};
        self.settings       = {};
        self.link           = self.fetchLink();
        self.browserWindow  = 'Chrome';
        
        self.driver         = None;
        self.proxy          = None;
        self.port           = None;
        self.useragent      = None;
        self.campaign       = None;
        self.ipSelected     = None;
        self.pid            = None;
        
        self.dataFile       = self.path + self.sep + "data" + self.sep + Renewer.hosttype + self.sep + 'data_' + TimeFn.getUnixTime() + '.xml';
        self.proxyfile      = self.path + self.sep + "Proxies.txt";
        self.uafile         = self.path + self.sep + "UserAgents.txt";
        
        # ----------------------------- <Driver Path> ------------------------------ #
        self.driverPath     = self.path + self.sep + "drivers";
        self.ccleaner       = self.driverPath + self.sep + "ccleaner"  + self.sep + "CCleaner.exe";
        self.chromeDriver   = self.driverPath + self.sep + "chromedriver.exe";
        self.firefoxDriver  = self.driverPath + self.sep + "geckodriver.exe";
        self.phantomJSDriver= self.driverPath + self.sep + "phantomjs.exe";
        
        self.logger         = LogFn(self.path, Renewer.hosttype);
    
    def fetchLink(self):
        ltype = '/replacer/sold'
        if (Renewer.jobtype == 'price'):
            ltype = '/replacer/price'
        elif (Renewer.jobtype == 'specific'):
            ltype = '/replacer/specific'
        
        return self.posterHost() + ltype;
    
    def posterHost(self):
        if (Renewer.hosttype == 'preowned'):
            return "http://xyz.com";
        elif (Renewer.hosttype == 'myleadTest'):
            return "http://xyz.com";
        else:
            return "http://xyz.com";
    
    ##################################### -------------- FILE FUNCTIONS ---------------- ##########################################
    
    def startReplacing(self):
        rootAd = FileFn.getAd(self.dataFile);
        for ad in rootAd.findall('ad'):
            self.logger.logInfo("starting replacer..");
            try:
                deleteSold = format(ad.find('deleteSold').text);
                isSold = format(ad.find('isSold').text);
                if deleteSold == '1' and isSold == 'Y':
                    xmpType = 'DELETESOLD';
                else:
                    xmpType = format(ad.find('XMLTYPE').text);

                title = format(ad.find("title").text);
                location = format(ad.find("location").text);
                description = format(ad.find("description").text);
                price = format(ad.find("price").text);
                link = format(ad.find("editLink").text);
                zip = format(ad.find('address').find('zip').text);
                modelYear = format(ad.find('year').text);
                makeModel = format(ad.find('makeModel').text);
                editContent = format(ad.find('replaceContent').text);
                editImages = format(ad.find('replacePics').text);
                editMap = format(ad.find('replaceMaps').text);
                
                st = True;
                self.logger.logInfo("Replacing ad - " + link);
                self.browser.redirect(link);
                
                if self.driver.title.find('manage posting') != -1:
                    if xmpType == 'DELETESOLD':
                        source = self.browser.pageSource();
                        if source.find('This posting has been deleted from craigslist') != -1:
                            self.postback(ad);
                            return True;
                        
                        self.logger.logInfo(" ## --- < Deleting Ads > --- ##");
                        self.browser.findByXPath("//input[@class='managebtn' and @name='go' and @value='Delete this Posting' and @type='submit']");
                        source = self.browser.pageSource();
                        if source.find('This posting has been deleted from craigslist') != -1:
                            self.logger.logInfo(" ## --- < Postback Started! > --- ##");
                            self.postback(ad);
                            self.logger.logInfo(" ## --- < Postback Done! > --- ##");
                            return True;
                    else:
                        source = self.browser.pageSource();
                        if source.find('This posting has been deleted from craigslist') != -1:
                            self.browser.findByXPath("//input[@type='submit' and @name='go' and @value='Undelete this Posting' and @class='managebtn']");
                            
                        if editContent == "1" and st == True:
                            self.browser.findByXPath("//input[@class='managebtn' and @name='go' and @value='Edit this Posting' and @type='submit']");
                            if self.driver.title.find('edit posting') != -1:
                                st = self.fillForm(ad);
                                source = self.browser.pageSource();
                                if source.find('Your posting will expire from the site') != -1:
                                    if st == True:
                                        self.logger.logInfo("## --- <Content Updated!> -- ##");
                                else:
                                    if self.driver.title.find('add map') != -1:
                                        st = self.editMap(ad);
                                        if st == True:
                                            self.logger.logInfo("## --- <Map Updated!> -- ##");
                                            editMap = 0;
                                        
                        if editImages == "1" and st == True:
                            st = self.uploadImages(ad);
                            if st == True:
                                self.logger.logInfo("## --- <Images Uploaded!> -- ##");
                        
                        if editMap == "1" and st == True:
                            st = self.redirectToMap(ad);
                            if st == True:
                                self.logger.logInfo("## --- <Map Updated!> -- ##");
                    
                    self.logger.logInfo("## --- <Final Step to Publish the Post> -- ##");
                    source = self.browser.pageSource();
                    
                    if self.finalStep(ad):
                        self.logger.logInfo(" ## --- < Postback Started! > --- ##");
                        self.postback(ad);
                        self.logger.logInfo(" ## --- < Postback Done! > --- ##");
                else:
                    self.logger.logInfo(" Error -- " + format(self.browser.getTextByXPath("//html//body")));
            except Exception as ex:
                self.logger.errorTrigger("Cant Renews Ads - " + format(ex));
                return False;
                
        return True;
    
    
    def finalStep(self, ad):
        #pgSource = format(self.browser.getTextByXPath("//html//body"));
        #self.logger.logInfo("Page Source -- " + pgSource);
        if self.clickPublish():
            if self.browser.pageTitle('edit posting') != -1:
                self.clickPublish();
        else:
            return False;

        source = self.browser.pageSource();
        if source.find('Thanks for posting with us') != -1 or source.find('We really appreciate it') != -1:
            self.logger.logInfo("Posting Successful!");
            return True;
        
        self.logger.logInfo("Posting Failed! - " + format(self.browser.getTextByXPath("//html//body")));
        return False;
        
        '''
        try:
            main_window = self.driver.current_window_handle;
            time.sleep(2);
            self.FindByXPath('//a[@target="_blank"]');
            time.sleep(2);
            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            self.driver.switch_to_window(main_window)
        except Exception as ex:
            pass;
        return True;
        '''
    
    def clickPublish(self):
        try:
            self.browser.findByXPath("//button[@class='button' and @type='submit' and @name='go' and @value='Continue']");
            return True;
        except Exception as ex:
            try:
                self.browser.pageReload();
                self.browser.findByXPath("//button[@class='button' and @type='submit' and @name='go' and @value='Continue']");
                return True;
            except Exception as ex:
                self.logger.errorTrigger('ELEMENT_FIND_ERROR', "Cannot Find Element - " + format(self.logger.printExp()));
                return False;
                
    def postback(self, ad):
        try:
            str = '';
            str += '&postId='   + format(ad.find('postingId').text);
            str += '&title='    + urlParser.pathname2url(format(ad.find('title').text));
            str += '&location=' + urlParser.pathname2url(format(ad.find('location').text));
            str += '&price='    + format(ad.find('originalPrice').text);
            
            link = self.posterHost() + '/replacer/save-post?' + str;
            
            print('\r\nPOSTBACK URL -' + link);
            FileFn.urlTrigger(link);
            #self.browser.redirect(link);
            #self.browser.findByXPath("//button[@type='submit']");
            
            return True;
            
        except Exception as ex:
            print(format(ex));
            return False;
            
    ############################# ----------- <Webdriver Initialization> --------------- #########################
    def initDriver(self):
        try:
            if self.browserWindow == 'Chrome':
                print(" ----- Chrome ---- ");
                #userProfile = "C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\";
                options = webdriver.ChromeOptions();
                options.add_argument("--headless") # Runs Chrome in headless mode.
                options.add_argument('--no-sandbox') # # Bypass OS security model
                options.add_argument('start-maximized')
                options.add_argument('disable-infobars')
                options.add_argument("--disable-extensions")
                options.add_argument('--disable-gpu')  # Last I checked this was necessary.
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"]);
                options.add_argument('--disable-webrtc');
                options.add_argument('--disable-geolocation');
                options.add_argument("--disable-application-cache");
                
                if self.useragent:
                    options.add_argument('--user-agent=' + self.useragent);
                
                if self.proxy:
                    proxy = self.proxy + ":" + self.port;
                    options.add_argument('--proxy-server=%s' % proxy);
                
                self.driver = webdriver.Chrome(options=options, executable_path=self.chromeDriver);
                #self.driver = webdriver.Ie();
            elif self.browserWindow == 'Firefox':
                print(" ----- Firefox ---- ");
                fp = webdriver.FirefoxProfile();
                fp.set_preference("browser.urlbar.autocomplete.enabled", False);
                fp.set_preference("browser.privatebrowsing.autostart", True);
                fp.set_preference('network.http.max-connections',                       30);
                fp.set_preference('network.http.max-connections-per-server',            30);
                fp.set_preference('network.http.pipelining.maxrequests',                0);
                fp.set_preference('network.http.max-persistent-connections-per-proxy',  0);
                fp.set_preference('network.http.max-persistent-connections-per-server', 0);
                
                if self.useragent:
                    fp.set_preference("general.useragent.override", self.useragent);
                
                if self.proxy:
                    fp.set_preference('network.proxy.ssl', self.proxy);
                    fp.set_preference('network.proxy.ssl_port', int(self.port));
                    fp.set_preference('network.proxy.http', self.proxy);
                    fp.set_preference('network.proxy.http_port', int(self.port));
                    fp.set_preference('network.proxy.type', 1);
                    
                self.driver = webdriver.Firefox(firefox_profile=fp, executable_path=self.firefoxDriver);
                #self.driver = webdriver.Firefox();
            elif self.browserWindow == 'PhantomJS':
                print(" ----- Phatmom Js ---- ");
                proxy = self.proxy + ":" + self.port;
                service_args = [
                    '--proxy=' + proxy,
                    '--proxy-type=socks5',
                ]
                self.driver = webdriver.PhantomJS(self.phantomJSDriver, service_args=service_args);
                self.driver.set_window_size(1120, 550);
                
            self.driver.maximize_window();
            self.driver.set_page_load_timeout(15);
            self.driver.implicitly_wait(15);
            
            #self.SetPid(self.browser);
            self.browser = BrowserFn(self.driver);
        except Exception as err:
            self.logger.errorTrigger("Cannot Initialize Webdriver - " + format(self.logger.printExp()));
            return False;

    
    ############################# ----------- <Fill Form Fields> --------------- #########################
    def fillForm(self, ad):
        self.logger.logInfo(" ## --- <Entered ad editing> -- ##");
        try:
            #---------------------- Title --------------------------#
            postingTitle = html.unescape(ad.find('title').text);
            if postingTitle:
                self.browser.fastFillByName("PostingTitle", postingTitle);
            
            
            #---------------------- PRICE --------------------------#
            if ad.find('price').text:
                price = int(ad.find('price').text);
                if price > 0:
                    self.browser.fastFillByName("price", format(price));
                else:
                    self.browser.fastFillByName("price", "");
            else:
                self.browser.fastFillByName("price", "");
            
            #---------------------- Location --------------------------#
            locName = ad.find('location').text;
            if locName:
                try:
                    self.browser.fastFillByName("GeographicArea", locName);
                except Exception as ex:
                    pass;
                    
            
            #------------------------- Postal Code ---------------------#
            postal = ad.find('address').find('zip').text;
            if postal:
                self.browser.fastFillByName('postal', postal);
            
            
            
            
            #------------------------- Description ---------------------#
            postingBody = ad.find('description').text;
            if postingBody:
                self.browser.fastFillByName('PostingBody', postingBody);
            
            #------------------------- Email Relay ---------------------#
            if ad.find('clRelay').text == "C":
                self.browser.findByXPath("//input[@name='Privacy' and @type='radio' and @value='C']");
            else:
                self.browser.findByXPath("//input[@name='Privacy' and @type='radio' and @value='A']");
            
            #------------------------- Phone Number ---------------------#
            if ad.find('showPhoneNumber').text == "1":
                if ad.find('phone').text:
                    if self.browser.isChecked('contact_phone_ok') == False:
                        self.browser.clickById("contact_phone_ok");
                    self.browser.fastFillByName('contact_phone', ad.find('phone').text);
            else:
                if self.browser.isChecked('contact_phone_ok') == True:
                        self.browser.clickById("contact_phone_ok");
                self.browser.fastFillByName('contact_phone', "");
                
            #---------------------- Dealer Full Name ---------------------#
            if ad.find('showContactName').text:
                self.browser.fastFillByName('contact_name', ad.find('showContactName').text);
            
            if ad.find('category').text == "trb":
                self.browser.fastFillByName('sale_manufacturer', ad.find('make').text);
                self.browser.fastFillByName('sale_model', ad.find('model').text);
                self.browser.fastFillByName('year_manufactured', ad.find('year').text);
            else:
                # FIX VIN UPDATE JOB
                self.browser.fastFillByName('auto_vin', ad.find('vin').text);
                #---------------------- Extra Fields -------------------------#
                self.fillExtraFields(ad);
            
            #----------------------------- Map ---------------------------#
            if ad.find('showMap').text == "1":
                self.browser.fastFillByName("xstreet0", ad.find('address').find('street').text);
                #self.browser.fastFillByName("xstreet1", ad.find('address').find('crossstreet').text);
                self.browser.fastFillByName("city", ad.find('address').find('city').text);
                #self.browser.fastFillByName("region", ad.find('address').find('state').text);
            
            # CLICK ENTER ON CITY FIELD TO MOVE TO NEXT PAGE
            
            self.browser.sendEnter("contact_name");
            return True;
            
            #self.browser.sendEnter("contact_name");
            #self.browser.findByXPath("//button[@name='go' and @type='submit' and @value='continue']");
            
            # source = self.browser.pageSource();
            # print(source);
            # os._exit(1);
            # if source.find('this is an unpublished draft') == -1:
                # self.browser.findByXPath("//button[@name='go' and @type='submit' and @value='continue']");
                # source = self.browser.pageSource();
                # if source.find('this is an unpublished draft') == -1:
                    # self.browser.findByCss("go big-button submit-button");
            
            #self.browser.findByXPath("//button[@name='go' and @type='submit' and @value='continue']");
            #self.browser.findByCss("go big-button submit-button");
            return True;
            
        except Exception as ex:
           self.logger.errorTrigger('UNKNOWN', 'Error on Selecting Optional Values - ' + format(ex) + ' ::: ' +  format(self.logger.printExp()));
           return False;
    
    
    ############################# ----------- <Fill Extra Fields> --------------- ##########################
    def fillExtraFields(self, ad):
        cat = ad.find('category').text;        
        try:
            #self.browser.selectByVal("auto_transmission", ad.find('transmission').text);
            self.browser.js("document.getElementsByName('language')[0].value=5;");
            self.browser.js("document.getElementsByName('auto_transmission')[0].value=" + ad.find('transmission').text + ";");
            
            #Cylinder type
            self.browser.js("document.getElementsByName('auto_cylinders')[0].value=" + ad.find('cylindersType').text + ";");
            
            #self.browser.selectByVal("auto_year", ad.find('year').text);
            self.browser.js("document.getElementsByName('auto_year')[0].value=" + ad.find('year').text + ";");
            
            #self.browser.fastFillByName('auto_make_model', ad.find('makeModel').text);
            #self.browser.selectByText("auto_fuel_type", ad.find('fuelTypeName').text);
            # Auto Paint Car
            self.browser.js("document.getElementsByName('auto_paint')[0].value=" + ad.find('paintColor').text + ";");
            
            if ad.find('odometer').text and int(ad.find('odometer').text) > 0:
                #self.browser.fastFillByName("auto_miles", ad.find('odometer').text);
                self.browser.js("document.getElementsByName('auto_miles')[0].value=" + ad.find('odometer').text + ";");
            
            print("Updated Transmission - OTHER FIELDS");
            return True;
        except Exception as ex:
            self.logger.errorTrigger('UNKNOWN', 'Error on Selecting Optional Values - ' + format(self.logger.printExp()));
            return False;
    
    # Upload images
    def uploadImages(self, ad):
        #return True;
        try:
            try:
                self.browser.findByXPath("//button[@name='go' and @type='submit' and @value='Edit Images']");
            except Exception as ex:
                self.browser.findByXPath("//input[@name='go' and @type='submit' and @value='Update Images' and @class='managebtn']");
            
            self.logger.logInfo(" ## --- <Images Upload Started> -- ##");
            vin         = ad.find('vin').text;
            upload      = 0;
            urls        = ad.find('images');
            if not urls:
                return True;
            
            urls = urls.findall('url');
            
            if self.delImages(ad):
                #self.browser.clickById("classic");
                for image in urls:
                    file = image.text;
                    file = file.replace('\\', '/').replace('//feed-app/feed-proauto', '/mnt/feed');
                    #self.browser.pageReload();
                    #file = self.path + self.sep + "test.jpg"
                    if os.path.isfile(file):
                        self.browser.findByXPath("//div[@class='moxie-shim moxie-shim-html5']//input[@type='file']", file);
                        self.logger.logInfo(" ## --- <Upload Image> -- ");
                        TimeFn.delayBySecs(2);
                        #self.browser.findByXPath("//input[@name='file' and @type='file']", file);
                
                TimeFn.delayBySecs(10);
                if (self.finishUpload()):
                    self.logger.logInfo(" ## --- <All Images Uploaded> -- ##");
                    return True;
                else:
                    self.logger.errorTrigger('IMAGES_UPLOAD_ERROR', format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
                    return False;
            else:
                return False;
        except Exception as ex:
            self.logger.errorTrigger('IMAGES_UPLOAD_ERROR', format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
            return False;
    
    def redirectToMap(self, ad):
        try:
            try:
                self.logger.logInfo(" ## --- Trying to find button Edit Location -- ##");
                self.browser.findByXPath("//form//button[@type='submit' and @name='go' and @value='Edit Location']");
            except Exception as ex:
                self.browser.findByXPath("//input[@name='go' and @type='submit' and @value='Edit Location' and @class='managebtn']");
            return self.editMap(ad);
            
        except Exception as ex:
            self.logger.errorTrigger('MAP_UPDATE_ERROR', format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
            return False;
    
    # Edit Map
    def editMap(self, ad):
        #return True;
        try:
            self.logger.logInfo(" ## --- <Map Updation Started> -- ##");
            self.browser.fastFillByName("xstreet0", ad.find('address').find('street').text);
            #self.browser.fastFillByName("xstreet1", ad.find('address').find('crossstreet').text);
            self.browser.fastFillByName("city", ad.find('address').find('city').text);
            self.browser.fastFillByName("postal", ad.find('address').find('zip').text);
            #Click on find button
            self.browser.findByXPath("//button[@id='search_button' and @class='mediumbutton' and @type='submit']");            
            
            #Add Marker to Map
            try:
                # temporarily make parent(assuming its id is parent_id) visible
                self.browser.js("document.getElementById('draggedpin').value = '1';");
                self.browser.js("document.getElementById('curlat').value = '" + ad.find('address').find('latitude').text + "';");
                self.browser.js("document.getElementById('curlng').value = '" + ad.find('address').find('longitude').text + "';");
            except Exception as ex:
                print(ex);
                pass;
                
            TimeFn.delayBySecs(3);
            self.browser.findByCss("button.bigbutton");
            return True;
        except Exception as ex:
            self.logger.errorTrigger('MAP_UPDATE_ERROR', format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
            return False;
    
    ############################# ----------- <Object Destroy Function> --------------- ##########################
    
    def finishUpload(self):
        try:
            self.browser.findByCss("button.bigbutton");
        except Exception as ex:
            try:
                self.browser.pageReload();
                self.browser.findByXPath("//button[@name='go' and @type='submit' and @value='Done with Images']");
            except Exception as ex:
                self.logger.errorTrigger('ELEMENT_FIND_ERROR', "Cannot Find Images Done button Element - " + format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
                return False;
        
        return True;
    
    def destroyObject(self):
        self.driver.close();

    def quitObject(self):
        try:
            print("Quitting Object");
            
            self.driver.close();
            self.driver.quit();
            
            self.browser.close();
            self.browser.quit();
        except Exception as ex:
            pass;
    
    def tearDown(self):
        self.quitObject();
    
    def delImages(self, ad):
        try:
            self.logger.logInfo("--- Started Deleting Images ---- ");
            imgCount = self.browser.findCountByXpath("//button[@type='submit' and @name='go' and @value='[x]']");
            imgCount = imgCount - 1;
            if imgCount <= 1:
                self.browser.pageReload();
                imgCount = self.browser.findCountByXpath("//button[@type='submit' and @name='go' and @value='[x]']");
                imgCount = imgCount - 1;
           
            self.logger.logInfo(" --- Total images %d --- " % imgCount);
            count = 1;
            TimeFn.shortDelay();
            
            if imgCount > 0:
                while count <= imgCount:
                    self.logger.logInfo(" --- Deleting Image %d --- " % count);
                    self.browser.findByXPath("//button[@name='go' and @type='submit' and @title='delete image' and @value='[x]']");
                    count += 1;
                    TimeFn.veryShortDelay();
            imgCount = self.browser.findCountByXpath("//button[@type='submit' and @name='go' and @value='[x]']");
        except Exception as ex:
            self.logger.errorTrigger('IMAGES_DELETE_ERROR', format(ad.find('fullDealername').text) + ' - ' + format(ad.find('posturl').text));
            return imgCount, count;
        
        return True;
    
    ############################# ----------- <Main Function> --------------- ###################################
    def test_renew(self):
        while(1):
            initialize = False;
            try:
                if not os.path.isfile(self.proxyfile):
                    self.logger.errorTrigger("Proxy File Not exist - " + self.proxyfile);
                    os._exit(1);
               
                self.proxy, self.port = FileFn.readProxy(self.proxyfile);
                self.logger.logInfo("## Proxy Used - %s ##" % self.proxy);
                
                #self.useragent = FileFn.readUseragent(self.uafile);
                #self.logger.logInfo("## " + self.useragent + " ##");
                
                self.quitObject();
                if not self.initDriver() == False:
                    self.logger.logInfo("## ------- Intializing Drivers --------- ##");
                    initialize = True;
                    if (FileFn.putXml(self.link, self.dataFile)):
                        if FileFn.checkXmlFormat(self.dataFile):
                            self.startReplacing();
                        else:
                            print("########## --- No Record found! ------ ###############");
                            TimeFn.delayBySecs(120);
                    else:
                        self.logger.errorTrigger("Cannot parse link to data file .. " + self.link);
                    
            except Exception as ex:
                self.logger.errorTrigger("Page Load TimeOut - " + format(self.proxy) + ":" + format(self.port) +  " ::: " + format(self.logger.printExp()));
    

if __name__ == "__main__":
    argvc = len(sys.argv);
    if (argvc > 1):
        Renewer.hosttype = sys.argv[1];
        if (argvc > 2):
            Renewer.jobtype = sys.argv[2];
    del sys.argv[1:]
    unittest.main();
