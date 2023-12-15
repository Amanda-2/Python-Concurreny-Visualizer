import logging
import socket
import datetime

# def current_time():
#     return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

# class SocketHandler(logging.Handler):
#     def __init__(self, host, port):
#         super().__init__()
    #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         self.client_socket.connect((host, port))
    #     except socket.error as e:
    #         print(f"Failed to connect to socket at {host}:{port}. Error: {e}")

    # def emit(self, record):
    #     try:
    #         log_entry = self.format(record)
    #         self.client_socket.sendall(log_entry.encode())
    #     except socket.error:
    #         self.handleError(record)

def setup_logging(file_name, port):
    with open(file_name, 'w'):
        pass

    logger = logging.getLogger('my_app')
    logger.setLevel(logging.INFO)

    # File Handler with dynamic filename
    fh = logging.FileHandler(file_name)
    # fh.setLevel(logging.INFO)

    # Socket Handler with dynamic port
    # sh = SocketHandler('localhost', port)
    # sh.setLevel(logging.INFO)

    # Formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(message)s')
    # fh.setFormatter(formatter)
    # sh.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    # logger.addHandler(sh)

    return logger
