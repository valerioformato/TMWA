export SECRET_KEY='$kwgj$mr@q4@)cktzug*&y9xx#tya3%-c)rss3q+1xv-8_40#3'
export DBROOTFILES=/Data/CalFiles

sleep 15s
celery -A TMWA.celeryapp worker -l info -E
