# run once a day at 6am
0 6 * * * curl http://cinema-stage.herokuapp.com/scrape/ >> /home/atkm/code/cinema/cron.log 2>&1
