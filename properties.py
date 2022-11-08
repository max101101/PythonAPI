"""
properties.py -- external configuration
"""

# Server parameters
db_name = "db/mydatabase.db"

# Worker parameters
football_api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

football_api_querystring = {"live":"all"}

football_api_headers = { 
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": ""
}

worker_sleep_time = 60
