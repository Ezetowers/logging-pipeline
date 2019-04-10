import threading

from log_file_manager import LogFileManager
from db_handlers import ReaderDbHandler, WriterDbHandler

HOST = '0.0.0.0'
WRITER_PORT = 6061
READER_PORT = 6071

def main():
    logs = LogFileManager()

    writer = WriterDbHandler(logs, HOST, WRITER_PORT)
    reader = ReaderDbHandler(logs, HOST, READER_PORT)

    reader.start()
    writer.start()

    while reader.is_alive() and writer.is_alive():
        try:
            reader.join()
            writer.join()
        except KeyboardInterrupt:
            print("Ctrl-c received! Sending kill to threads...")
            reader.stop()
            writer.stop()

    print("Termine")

if __name__ == '__main__':
    main()
