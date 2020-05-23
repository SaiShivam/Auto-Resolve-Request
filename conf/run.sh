cd /home/DS/ads.bsai/Autoresolve-CAP
export LD_LIBRARY_PATH=/home/DS/ads.bsai/anaconda3/lib:$LD_LIBRARY_PATH
source /home/DS/ads.bsai/anaconda3/bin/activate /home/DS/ads.bsai/Autoresolve-CAP/env/autoresolve_env
uwsgi --ini /home/DS/ads.bsai/Autoresolve-CAP/conf/uwsgi.ini