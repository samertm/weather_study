# run_weather_requests.sh
# Run weather study's `requests.py` within the master branch.
# David Prager Branner
# 20140523

cd /home/dpb/github_public/weather_study
git checkout master
source v_env3/bin/activate
cd CODE
python requests.py
