# json-logger
## Dependencies
install `python-json-logger`

```
pip3 install python-json-logger
```

## Usage Example
NOTICE: the example assumes that logger.py is in the same directory as your calling module, else a different import method should be used
```
import os, sys
from logger import JSONLogger

# logging config yaml file path
LOG_CONFIG_PATH = os.environ.get('LOG_CONFIG_PATH', 'log.yaml')
APP_NAME = 'my-service'

# there should be a formatter that uses these fields in configuration yaml (e.g. format: '%(timestamp)s %(service)s')
additional_constant_fields = {'service': APP_NAME}

# NOTICE: there should be a matching logger name in configuration yaml (e.g. main-debug)
log = JSONLogger('main-info', LOG_CONFIG_PATH, additional_constant_fields).get_logger()

log.critical('system crashed')
log.error('incorrect input')
log.warn('not ready')
log.info('some info', extra={'action_id': 3}) # extra fields
log.debug('some info', extra={'action_id': 4}) # will not be logged because logger level set to INFO ('main-info')
```

## Example Configuration YAML
```
version: 1
formatters:
  brief:
    format: '%(message)s'
  json:
    format: '%(timestamp)s %(service)s %(loglevel)s %(message)s'
    class: logger.CustomJsonFormatter
handlers:
  console:
    class: logging.StreamHandler
    formatter: json
    stream: ext://sys.stdout
  file:
    class : logging.handlers.RotatingFileHandler
    formatter: json
    filename: logfile.log # log files full path
    maxBytes: 5242880 # 5 MB
    backupCount: 10
loggers:
  main-debug:
    handlers: [console, file]
    level: DEBUG
  main-info:
    handlers: [console, file]
    level: INFO
  main-warning:
    handlers: [console, file]
    level: WARNING
  main-error:
    handlers: [console, file]
    level: ERROR
  main-critical:
    handlers: [console, file]
    level: CRITICAL
```