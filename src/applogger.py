""" Logging """
import os
import logging
import logging.config
import logging.handlers

def logger_setup(logname):
    """ Defining the logging method """
    logger = logging.getLogger(logname)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(os.getcwd()+'/logs/ARRapp.log', maxBytes=10485760, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
