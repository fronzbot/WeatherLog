import configparser
import time
import os
import pyowm

INFO = None
CONFIG_PATH = None

def main():
  if CONFIG_PATH is None:
    raise ValueError("Please set CONFIG_PATH variable to location of config.ini")
  INFO = get_info()
  Weather = WeatherLog(INFO, debug=True)
  start = time.time()
  time.clock()
  elapsed = 0
  while elapsed < INFO['RUNTIME']:
    Weather.run(elapsed)
    time.sleep(INFO['INTERVAL'])
    elapsed = time.time() - start
    

def get_info():
  '''
  Function to get setup information from info file
  '''
  Config = configparser.ConfigParser()
  Config.read(CONFIG_PATH+"/config.ini")
  
  try:
    API = ConfigSectionMap(Config, "Setup")["api"]
  except:
    raise KeyError("Exception on 'api' option!")
    
  try:
    LOCATION = ConfigSectionMap(Config, "Setup")["location"]
  except:
    raise KeyError("Exception on 'city' option!")
    
  try:
    LOGPATH = ConfigSectionMap(Config, "Setup")["logpath"]
  except KeyError:
    LOGPATH = os.path.dirname(os.path.abspath(__file__))
    
  try:
    INTERVAL = ConfigSectionMap(Config, "Setup")["interval"]
    INTERVAL = float(INTERVAL)
    if INTERVAL < 1:
      raise ValueError("Interval for Weather calls cannot be less than 1 second!")
  except KeyError:
    INTERVAL = 60
    
  try:
    RUNTIME = ConfigSectionMap(Config, "Setup")["runtime"]
    RUNTIME = float(RUNTIME)
  except KeyError:
    RUNTIME = 60*60*8
    
  try:
    TEMPUNITS = ConfigSectionMap(Config, "Setup")["temp_unit"]
  except KeyError:
    TEMPUNITS = 'fahrenheit'
    
  return {'API':API, 'LOCATION':LOCATION, 'LOGPATH':LOGPATH, 'INTERVAL':INTERVAL, 'RUNTIME':RUNTIME, 'TEMPUNITS':TEMPUNITS}

  
def ConfigSectionMap(Config, section):
  # From: https://wiki.python.org/moin/ConfigParserExamples
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1   

 
class WeatherLog(object):
  '''
  Class to get weather and send to a log file
  '''
  def __init__(self, info, debug=False):
    self.debug = debug
  
    self.humidity = 0
    self.temperature = 0
    self.pressure = 0
    self.cloud_coverage = 0
    self.windspeed = 0
    
    self.api = info['API']
    self.logpath = info['LOGPATH']
    self.location = info['LOCATION']
    self.tempunits = info['TEMPUNITS']
    
    self.logfile = self.logpath + '/weather_log_' + time.strftime("%Y_%m_%d__%H_%M_%S") + '.txt'
    
    log = open(self.logfile, "w")
    log.write('Time\tTemp\tHumidity\tPressure\tWindspeed\tCloud Coverage\n')
    log.close()

    self.owm = pyowm.OWM(self.api)
    
    if self.debug:
      print("API = " + self.api)
      print("LOGPATH = " + self.logpath)
      print("LOCATION = " + self.location)
      print("TEMPUNITS = " + self.tempunits)
      print("INTERVAL = " + str(info['INTERVAL']))
      print("RUNTIME = " + str(info['RUNTIME']))
      print("LOGFILE is " + self.logfile)
    
  def run(self, elapsed):
    observation = self.owm.weather_at_place(self.location)
    self.get_weather(observation)
    self.write_to_log(observation, elapsed)
  
  def get_weather(self, observation):
    w = observation.get_weather()
    self.humidity = w.get_humidity()
    self.temperature = w.get_temperature(self.tempunits)['temp']
    self.pressure = w.get_pressure()['press']
    self.cloud_coverage = w.get_clouds()
    self.windspeed = w.get_wind()['speed']
    
  def write_to_log(self, data, elapsed):
    data_string = str(elapsed) + '\t' + str(self.temperature) + '\t' + str(self.humidity) + '\t' + str(self.pressure) + '\t' + str(self.windspeed) + '\t' + str(self.cloud_coverage) + '\n'
    if self.debug:
      print('Writing: ' + data_string)
    log = open(self.logfile, "a")
    log.write(data_string)
    log.close()
    
if __name__ == "__main__":
  main()
  