- TODO:
    + Cron job. How to handle error when a daily scraping fails?
    + Make tests work with rq+workers.

- Thoughts:
    + How are timezones handled?
    + Denormalize tables?
    + When do showtimes for each week become available?
    + How to transfer local data to the deployed db?
    + Distribute jobs to multiple workers.

- Tests:
    + pytest. Run with `python -m pytest`.
        Just `pytest` won't be able to find the app.

- Heroku stage (production):
    + ensure Procfile
    + enable heroku-postgresql:hobby-dev addon
    + heroku config:set APP_SETTINGS=config.StagingConfig --remote stage (=config.ProductionConfig)
    + heroku config:set FLASK_APP=cinema --remote stage
    + heroku config:set FLASK_ENV=development --remote stage (=production)
    + heroku run flask db upgrade --remote stage
    + heroku addons:create redistogo:nano --remote stage

- Theaters
    + Good: Cinema Nova, Living Room Theater (Portland)
    + Local: Roxie, New Parkway, Shattuck, California, Elmwood
    + Bad: AMC Metreon 16, UA Berkeley 7

- Analytics:
    + Good theaters minus Bad, or 
    + Symmetric differences between good theaters.

- Data to collect:
    + Scrape the google showtimes api 
    + Keep date and film. Count the number of times a film is shown each day.

- showtime apis
    + Google showtimes API (https://www.google.com/movies/?near=berkeley): closed
    + http://developer.tmsapi.com/docs/data_v1_1/movies/Theatre_showtimes : not free
