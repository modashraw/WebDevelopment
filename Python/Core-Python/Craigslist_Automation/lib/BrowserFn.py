from selenium.webdriver.common.action_chains import ActionChains;
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys

from lib.TimeFn import TimeFn;
import pyperclip;

class BrowserFn():
    def __init__(self, obj):
        self.driver = obj;
    
    def redirect(self, path):
        self.driver.get(path);
        TimeFn.veryShortDelay();
    
    def scrollDown(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
            TimeFn.veryShortDelay();
            self.driver.execute_script("window.scrollTo(0, 0);");
        except Exception as ex:
            pass;
    
    def findByXPath(self, xpath, fill=False):
        element = self.driver.find_element_by_xpath(xpath);
        if fill == False:
            element.click();
        else:
            element.send_keys(fill);
        
        TimeFn.veryShortDelay();
    
    def clickById(self, id):
        TimeFn.veryShortDelay();
        self.driver.find_element_by_id(id).click();
    
    def clickByName(self, name):
        TimeFn.veryShortDelay();
        self.driver.find_element_by_name(name).click();
        
    
    def fastFillById(self, id, sendData):
        element = self.driver.find_element_by_id(id);
        element.clear();
        element.send_keys(sendData);
        TimeFn.shortDelay();
    
    def fastFillByName(self, name, sendData):
        element = self.driver.find_element_by_name(name);
        #self.actionMove(element)
        element.clear();
        element.send_keys(sendData);
    
    def slowFillByName(self, name, sendData):
        element = self.driver.find_element_by_name(name);
        element.clear();
        for x in range(len(sendData)):
            element.send_keys(sendData[x]);
            TimeFn.typingDelay();
    
    def slowFillById(self, id, sendData):
        element = self.driver.find_element_by_id(id);
        element.clear();
        for x in range(len(sendData)):
            element.send_keys(sendData[x]);
            TimeFn.typingDelay();
    
    
    def selectByVal(self, name, value):
        element = self.driver.find_element_by_name(name);
        #self.actionMove(element)
        Select(element).select_by_value(value);
        
    def selectByText(self, name, value):
        element = self.driver.find_element_by_name(name);
        #self.actionMove(element)
        Select(element).select_by_visible_text(value);
    
    def actionMove(self, element):
        try:
            ActionChains(self.driver).move_to_element(element).perform();
        except Exception as ex:
            pass;
        return True;
    
    def findByCss(self, xpath):
        element = self.driver.find_element_by_css_selector(xpath);
        #self.actionMove(element)
        element.click();
        TimeFn.veryShortDelay();
        
    def findTextByLink(self, txt):
        return self.driver.find_element_by_link_text(txt).text;
    
    def sendEnter(self, name):
        try:
            element = self.driver.find_element_by_name(name);
            element.send_keys(Keys.ENTER);
            #TimeFn.shortDelay();
            return True;
        except Exception as ex:
            print(format(ex));
        
        return False;
        
    def getTextByXPath(self, xpath):
        element = self.driver.find_element_by_xpath(xpath);
        #self.actionMove(element)
        txt = format(element.text);
        return txt;
    
    def paste_keys_id(self, id, data):
        pyperclip.copy(data)
        element = self.driver.find_element_by_id(id);
        ActionChains(self.driver).move_to_element(element).click(element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform();
        
    def paste_keys_name(self, name, data):
        pyperclip.copy(data)
        element = self.driver.find_element_by_id(name);
        ActionChains(self.driver).move_to_element(element).click(element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        
        
    def isChecked(self, name):
        checked = self.driver.find_element_by_name(name).is_selected();
        return checked
        
    def findCountByXpath(self, xpath):
        return len(self.driver.find_elements_by_xpath(xpath));
        
    def pageReload(self):
        self.driver.refresh();
        TimeFn.shortDelay();
    
    def pageTitle(self, match=None):
        if match is None:
            return self.driver.title;
        else:
            return self.driver.title.find(match);
    
    def pageSource(self):
        return self.driver.page_source;
    
    def js(self, code):
        self.driver.execute_script(code);