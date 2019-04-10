class WriterWorker(object):
    def __init__(self, logs, queue):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            skt = self.queue.get(True)
            print("---------------------------Agarre un pedido----------------------------------")
            write_info = skt.receive_write_info()
            print("---------------------------Recibo la info del pedido----------------------------------")
            self.logs.get_or_create_log(write_info.get_appId(), write_info.get_timestamp()).write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())
            print("---------------------------La escribi----------------------------------")
            skt.send_write_confirmation()
            print("---------------------------Envio la info de la escritura----------------------------------")
            skt.close()

class ReaderWorker(object):
    def __init__(self, logs, queue):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            skt = self.queue.get(True)
            print("---------------------------Agarre un pedido----------------------------------")
            read_info = skt.receive_read_info()
            print("---------------------------Lei la info del pedido----------------------------------")

            logs_to_read = self.logs.get_logs(read_info.get_appId(), read_info.get_from(), read_info.get_to())

            print("---------------------------Obtengo los logs a leer----------------------------------")

            logs_readed = []
            for log_to_read in logs_to_read:
                logs_readed += log_to_read.read_log(read_info.get_appId(), read_info.get_from(), read_info.get_to())
            print("---------------------------Lei los logs----------------------------------")
            skt.send_logs(logs_readed)
            print("---------------------------Envie los logs leidos----------------------------------")
            skt.close()
