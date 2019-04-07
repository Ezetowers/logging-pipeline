import multiprocessing

from log import Log
from reader_db_handler import ReaderDbHandler
from writer_db_handler import WriterDbHandler

HOST = '127.0.0.1'
WRITER_PORT = 6060
READER_PORT = 6070

def _spawn_reader(logs):
    reader = ReaderDbHandler(logs, HOST, READER_PORT)
    reader.run()

def _spawn_writer(logs):
    writer = WriterDbHandler(logs, HOST, WRITER_PORT)

def main():
    logs = {1: Log("1_log.csv")}

    reader = multiprocessing.Process(target=_spawn_reader, args=(logs))
    writer = multiprocessing.Process(target=_spawn_writer, args=(logs))

    reader.start()
    writer.start()

if __name__ == '__main__':
    main()
