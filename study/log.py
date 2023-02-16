import logging
import logging.handlers

log = logging.getLogger('snowdeer_log')
log.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('./log.txt')
streamHandler = logging.StreamHandler()

log.addHandler(fileHandler)
log.addHandler(streamHandler)

if __name__ == '__main__':
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')
    
# https://snowdeer.github.io/python/2017/11/17/python-logging-example/
# https://gonigoni.kr/posts/python-logging/