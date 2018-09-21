- TODO:
    + Scraping should happen at the start of a day (i18n is an issue), or only scrape information from future dates.
    + Delegate scraping jobs to workers at the /scrape endpoint.
    + Add a uniqueness constraint on the Showtime model by date,
        either at the model or application level.

- Tests:
    + pytest. Run with `python -m pytest`.
        Just `pytest` won't be able to find the app.

- Theaters
    + Cinema Nova
    + Living Room Theater (Portland)
    + Local: Roxie, New Parkway, Shattuck, California
    + Bad: AMC Metreon 16, UA Berkeley 7
- Product: find actually indie films
    + Good theaters - Bad, or 
    + Symmetric differences between good theaters.
- Data to collect:
    + Scrape the google showtimes api 
    + Keep date and film. Count the number of times a film is shown each day.
- showtime apis
    + Google showtimes API (https://www.google.com/movies/?near=berkeley): closed
    + http://developer.tmsapi.com/docs/data_v1_1/movies/Theatre_showtimes : not free
