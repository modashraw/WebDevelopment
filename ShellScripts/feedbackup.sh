#!/bin/bash

TIMESTAMP=`date +%Y%m%d`
DEST_DIR="/var/ftp/_feedbackups"

#DELETE 30 days old backup first
find ${DEST_DIR} -mtime +30 -exec rm {} \;

SRC_DIR="*"
FNAME="incoming-feed"
LOG="/root/backup/${FNAME}-${TIMESTAMP}.log"
echo -e "Starting backup of incoming feeds $SRC_DIR directory" >> $LOG
cd /var/ftp
tar -zcvf ${DEST_DIR}/${FNAME}-${TIMESTAMP}.tar.gz ${SRC_DIR} --exclude='_feedbackups' --exclude='pearson' >> $LOG
echo -e "Ending backup of incoming feeds $SRC_DIR" >> $LOG

rsync -v -rlgopa --delete --exclude "_feedbackups" --exclude "pearson" --exclude "*/.bash*" /var/ftp/ 192.168.245.88:/var/ftp

ssh 192.168.235.105 'service php-fpm restart'
/etc/init.d/php-fpm restart > /dev/null
/etc/init.d/nginx restart > /dev/null
