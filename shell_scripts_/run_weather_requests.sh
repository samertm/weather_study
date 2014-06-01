# run_weather_requests.sh
# Run weather study's `requests.py` within the master branch.
# David Prager Branner
# 20140601

cd /home/dpb/github_public/weather_study
source v_env3/bin/activate
cd code
python /home/dpb/github_public/weather_study/code/requests.py
git add -A /home/dpb/github_public/weather_study
git commit -m 'upload downloads from today'
