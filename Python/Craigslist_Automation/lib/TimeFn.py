import datetime;
import time;
import random;
import re;
class TimeFn():
    def getCurrentTime():
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        return currenttime;
    
    def getCurrentDate():
        currentdate = datetime.datetime.now().strftime("%Y-%m-%d");
        return currentdate;
    
    def shortDelay():
        time.sleep(random.randint(3, 7));
    
    def longDelay():
        time.sleep(random.randint(12, 17));
    
    def typingDelay():
        time.sleep(0.20);
    
    def veryShortDelay():
        time.sleep(float(format(random.uniform(1, 2), '.1f')));
    
    def getUnixTime():
        return format(int(time.time()));
        
    def delayBySecs(secs):
        time.sleep(secs);