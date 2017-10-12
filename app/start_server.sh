export SECRET_KEY='$kwgj$mr@q4@)cktzug*&y9xx#tya3%-c)rss3q+1xv-8_40#3'
export DBROOTFILES=/Data/CalFiles

python manage.py migrate
python manage.py updatedb
python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 8000 -v2 TMWA.asgi:channel_layer
