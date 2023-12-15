from flask import Flask, render_template, jsonify
import logging

app = Flask(__name__)
log_messages = []  # List to store log messages

class CustomLogHandler(logging.Handler):
    def emit(self, record):
        # Add the log record's message to the log_messages list
        log_messages.append(self.format(record))

# Setup logger and add the custom handler
logger = logging.getLogger('custom_logger')
logger.setLevel(logging.INFO)
logger.addHandler(CustomLogHandler())

# Endpoint to fetch log messages
@app.route('/test.txt')
def get_logs():
    return jsonify(log_messages)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this file is in your templates directory

if __name__ == '__main__':
    app.run(debug=True, port=5000)
