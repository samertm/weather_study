# run_weather_requests.sh
# Run weather study's `requests.py` within the master branch.
# David Prager Branner
# 20140523

cd /home/dpb/github_public/weather_study
echo `pwd`
source v_env3/bin/activate
cd CODE
echo `pwd`
python -c 'print("here within Python")'
/home/dpb/github_public/weather_study/CODE/requests.py
echo 'done with python'
git add -Av ..
git commit -m 'upload downloads from today'
echo 'done with git'
