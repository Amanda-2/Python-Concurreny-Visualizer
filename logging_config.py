import logging

def setup_logging(file_name, port):
    with open(file_name, 'w'):
        pass

    logger = logging.getLogger('my_app')
    logger.setLevel(logging.INFO)

    # File Handler with dynamic filename
    fh = logging.FileHandler(file_name)
    
    # Add handlers to logger
    logger.addHandler(fh)
    # logger.addHandler(sh)

    return logger
