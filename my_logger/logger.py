import os
import sys
from datetime import datetime


class Logger:
    def __init__(self, filename=None):
        self.log_dir = os.environ.get("LOG_PATH", "./output/log")
        os.makedirs(self.log_dir, exist_ok=True)
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.log"
        self.log_file = os.path.join(self.log_dir, filename)
        self.terminal = sys.stdout
        sys.stdout = self
        self.buffer = ""

    def write(self, message):
        """Rewrite the write method of stdout to buffer messages until they are complete."""
        self.terminal.write(message)
        self.buffer += message

        if "\n" in message:
            timestamp = self.get_timestamp()
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {self.buffer}")
            except Exception as e:
                self.terminal.write(f"Error writing to log file: {e}\n")
            self.buffer = ""

    def flush(self):
        """Rewriting the flush method of stdout"""
        self.terminal.flush()

        if self.buffer:
            timestamp = self.get_timestamp()
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {self.buffer}")
            except Exception as e:
                self.terminal.write(f"Error writing to log file: {e}\n")
            self.buffer = ""

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 示例用法
if __name__ == "__main__":
    os.environ["LOG_PATH"] = "./logs"

    logger1 = Logger("custom.log")
    print("这是自定义文件名的日志")

    logger2 = Logger()
    print("这是自动按时间命名的日志")