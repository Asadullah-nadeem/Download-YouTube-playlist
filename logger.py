class CustomLogger:
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def debug(self, msg):
        self.log_callback(msg)

    def warning(self, msg):
        self.log_callback(f"WARNING: {msg}")

    def error(self, msg):
        self.log_callback(f"ERROR: {msg}")
