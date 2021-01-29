import os;
import re;
import imaplib, email;

class Email():
    def getEmailHost(self, email):
        foundHost = re.search('([^\@]+)$', email).group(0);
        hostaddr = {};
        if foundHost:
            if foundHost == "gmail.com":
                hostaddr['host'] = "imap.gmail.com";
            elif (foundHost == 'hotmail.com' || foundHost == 'live.com'):
                hostaddr['host'] = "imap-mail.outlook.com";
            elif foundHost == 'yahoo.com':
                hostaddr['host'] = "imap.mail.yahoo.com";
            elif foundHost == 'aol.com':
                hostaddr['host'] = "imap.aol.com";
            else:
                hostaddr['host'] = "outlook.office365.com";
            
            hostaddr['port'] = 993;
            
            return hostaddr;

    def fetchemails(self, email, password, date, editLink):
        retLink = None;
        plink = None;
        
        hostaddr = self.getEmailHost(email);
        mail = imaplib.IMAP4_SSL(hostaddr['host'], hostaddr['port']);
        mail.login(email, password);
        mail.list();
        mail.select("inbox"); # connect to inbox.
        retCode, data = mail.uid('search', None, '(SENTSINCE {date} HEADER FROM "robot@craigslist.org")'.format(date=date));
        try:
            if retCode == "OK":
                print("Logged In to Account");
                ids = data[0]; # data is a list.
                id_list = ids.split(); # ids is a space separated string
                if id_list:
                    latest_email_uid = id_list[-1]; # get the latest
                    print("Latest Email Id");
                    resultOK, fetchedData = mail.uid('fetch', latest_email_uid, '(RFC822)');
                    if resultOK == "OK":
                        raw_email = fetchedData[0][1].decode("utf-8");
                        matchObj = re.search('https:\/\/post\.craigslist\.org\/[^\s]+', raw_email, re.M|re.I|re.U);
                        if (matchObj):
                            plink = matchObj.group(0);
                            if editLink == True:
                                return plink;
                            else:
                                retLink = self.returnLink(plink);
                        else:
                            self.logger.error('No Email Post Link Found:' + self.email + ' , Password: ' + self.emailpassword);
                            print('No Email Post Link Found:' + self.email + ' , Password: ' + self.emailpassword);
            else:
                self.logger.error('Cannot Logged In  --  email:' + self.email + ' , Password: ' + self.emailpassword);
                print('Cannot Logged In  --  email:' + self.email + ' , Password: ' + self.emailpassword);
            mail.close();
            mail.logout();
        except Exception as ex:
            self.logger.error(ex);
            print(ex);
        return(retLink, plink);