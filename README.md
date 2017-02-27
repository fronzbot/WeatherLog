# WeatherLog
Weather logging utility

# Description
Saves weather information from openweathermap to tab-delimited file over time.  Set WeatherLog.WeatherLog.CONFIG_PATH to location of a config.ini file which contains the following info:

```ini
[Setup]
api=YOUR_OPENWEATHERMAP_API_KEY
location=YOURLOCATION
logpath=PATH_WHERE_LOG_FILE_WILL_BE_SAVED
interval=HOW_OFTEN_TO_UPDATE_IN_SECONDS
runtime=HOW_LOG_TO_RUN_IN_SECONDS
temp_unit=UNIT_FOR_TEMPERATURE_MEASUREMENT
```

# Installation
Download latest release and use following command to install

`python setup.py install`
