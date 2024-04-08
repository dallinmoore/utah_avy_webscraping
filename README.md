# Scripts Overview - Utah Avalanche Center Webscraping

This repository contains several Python scripts related to processing and scraping the [Utah Avalanche Center Website](https://utahavalanchecenter.org/) to build a database of over 10,000 avalanche forecasts and reports. Each script serves a specific purpose as outlined below:

## add_rose_data.py

This script is responsible for adding forecast data to avalanche forecast datasets using the `process_rose_data.py` and `read_the_rose.py` script.

## add_rose_data_old.py

This is a version of the script `add_rose_data.py` used for an older version of the website.

## daily_avy_forecast.py

This script is used to fetch all links to avalanche forecasts from the website, to assure that all forecasts are accounted for.

## match_avy_danger.py

This script designed to match avalanche danger levels with every avalanche report to provide insights into the dangers forecasted before an avalanche occured.

## old_ut_avy_reports.py

This script retrieves all avalanche reports from the older version of the website.

## process_rose_data.py

This script scrapes the daily forecast webpage for the link to the png file to be used by the `read_the_rose.py` script.

## read_the_rose.py

This script processes a png of the rose forcast for the day, turning it into quantifiable data rather than an image.

## scrape_new_forecasts.py

This script is responsible for scraping all avalanche forecasts from the newer version of the website.
