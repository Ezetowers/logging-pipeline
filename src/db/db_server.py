import threading

from log_manager import LogManager
from db_handlers import ReaderDbHandler, WriterDbHandler

HOST = '0.0.0.0'
WRITER_PORT = 6061
READER_PORT = 6071

def _spawn_reader(logs):
    reader = ReaderDbHandler(logs, HOST, READER_PORT)
    reader.run()

def _spawn_writer(logs):
    writer = WriterDbHandler(logs, HOST, WRITER_PORT)
    writer.run()

def main():
    logs = LogManager()

    writer = threading.Thread(target=_spawn_writer, args=(logs,))
    reader = threading.Thread(target=_spawn_reader, args=(logs,))

    reader.start()
    writer.start()

    reader.join()
    writer.join()

if __name__ == '__main__':
    main()
