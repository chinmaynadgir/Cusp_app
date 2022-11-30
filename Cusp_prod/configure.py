import configparser
config = configparser.ConfigParser()
config['sql'] = {}
config['sql']['Host'] = 'localhost'
config['sql']['User'] = 'root'
config['sql']['password'] = '1024'
config['sql']['database'] = 'cuspera'
with open('config.ini', 'w') as configfile:
  config.write(configfile)