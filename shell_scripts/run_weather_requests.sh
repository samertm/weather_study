# run_weather_requests.sh
# Run weather study's `requests.py` within the master branch.
# David Prager Branner
# 20140523

cd /home/dpb/github_public/weather_study
source v_env3/bin/activate
cd CODE
/home/dpb/github_public/weather_study/CODE/requests.py
git-add -Av ..
git-commit -m 'upload downloads from today'
