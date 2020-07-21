from loguru import logger
class log:
    def setlog(self,level,msg):

        if level=='debug':
            logger.debug(msg)
        elif level=='info':
            logger.info(msg)
        elif level=='warning':
            logger.warning(msg)
        elif level=='error':
            logger.error(msg)

    def debug(self, msg):
        self.setlog('debug', msg)

    def info(self, msg):
        self.setlog('info', msg)

    def warning(self, msg):
        self.setlog('warning', msg)

    def error(self, msg):
        self.setlog('error', msg)

