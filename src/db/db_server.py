#Entry point for the database server of the logging pipeline
import os
import threading

from log_file_manager import LogFileManager
from db_handlers import ReaderDbHandler, WriterDbHandler

HOST = '0.0.0.0'
WRITER_PORT = 6061
READER_PORT = 6071

def main():
    number_of_threads = int(os.environ['NUMBER_OF_THREADS'])
    number_of_queued_connections = int(os.environ['MAX_QUEUED_CONNECTIONS'])
    logs = LogFileManager()

    writer = WriterDbHandler(logs, number_of_threads, number_of_queued_connections, HOST, WRITER_PORT)
    reader = ReaderDbHandler(logs, number_of_threads, number_of_queued_connections, HOST, READER_PORT)

    reader.start()
    writer.start()

    while reader.is_alive() and writer.is_alive():
        try:
            reader.join()
            writer.join()
        except KeyboardInterrupt:
            reader.stop()
            writer.stop()

if __name__ == '__main__':
    main()
