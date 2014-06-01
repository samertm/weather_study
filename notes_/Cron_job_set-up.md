## Cron job set-up

Using `crontab -e` (on Ubuntu installation) compose the following cron job:

    SHELL=/bin/bash
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
    
    # Run requests for Weather Study
    30 16 * * * /home/dpb/github_public/weather_study/shell_scripts/run_weather_requests.sh 

[end]
