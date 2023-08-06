import socket
from asyncio import wait_for
import asyncio
import errno
from basic_logtools.filelog import LogFile

from networktools.time import now
from networktools.library import my_random_string

from networktools.colorprint import rprint, bprint
from networktools.path import home_path


class BaseProtocol:
    """ Class to connect to tcp port and parse GSOF messages """
    tipo = "Base"

    def __init__(self, **kwargs):
        station = kwargs.get('code')
        self.sock = kwargs.get('sock')
        self.timeout = kwargs.get('timeout', 1)
        self.raise_timeout = kwargs.get('raise_timeout', False)
        self.raise_incompleteread = kwargs.get("raise_incomplete_read", False)
        self.max_try = kwargs.get("max_try", 3600)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.sock = self.create_socket(None)
        self.loop = kwargs.get('loop')
        self.station = station
        self.sock.settimeout(self.timeout)
        self.msg_dict = {}
        self.checksum = None
        self.try_connect = 0
        self.id_columns = {}
        self.keys = []
        self.status = False
        # manage asyncronous clients
        self.idc = []
        self.clients = {}
        log_path = home_path(
            kwargs.get('log_path', '~/gn_socket/logs')
        )
        log_level = kwargs.get('log_level', 'INFO')
        self.logger = LogFile(self.class_name,
                              station,
                              self.host,
                              path=log_path,
                              base_level=log_level)
        # manage asyncronous clients
        self.logger.info("Log para %s" % self.station)

    @property
    def class_name(self):
        return self.__class__.__name__

    def create_socket(self, sock):
        sock = None
        if sock is None:
            sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = sock
        return sock

    def off_blocking(self):
        self.sock.setblocking(False)

    def on_blocking(self):
        self.sock.setblocking(True)

    async def connect(self):
        host = self.host
        port = self.port
        loop = self.loop
        counter = 0
        while not self.status:
            if counter > self.max_try:
                counter = 0
            try:
                future_open_conn = asyncio.open_connection(
                    loop=loop,
                    host=host,
                    port=port)
                (reader, writer) = await asyncio.wait_for(
                    future_open_conn, timeout=self.timeout)
                idc = await self.set_reader_writer(reader, writer)
                hb = await self.heart_beat(idc)
                if hb:
                    self.status = True
                    self.logger.info("Conexion a %s realizada" % self.station)
                else:
                    self.logger.error(hb)
            except asyncio.TimeoutError as te:
                self.logger.exception(
                    f"Tiempo fuera en intento de conexión {te}, iteracion {counter}")
                counter += 1
                await asyncio.sleep(10+counter)
                continue
            except socket.timeout as timeout:
                self.on_blocking()
                self.logger.error(
                    f"Error en conexión con {host}:{port}, error: {timeout}, iteración {counter}")
                # print("Error de socket a GSOF en conexión %s" % timeout)
                counter += 1
                self.status = False
                await asyncio.sleep(10+counter)
                continue
                # await self.connect()
                # raise timeout
            except socket.error as e:
                self.status = False
                counter += 1
                self.on_blocking()
                if e.errno == errno.ECONNREFUSED:
                    # print("Conexión rechazada en %s" %
                    #      self.station, file=sys.stderr)
                    self.logger.exception(
                        f"Error al conectar {e}, station {self.station}, iteración {counter}")
                    counter += 1
                    await asyncio.sleep(10+counter)
                else:
                    # print("No se puede establecer conexión, de %s" %
                    #      self.station, file=sys.stderr)
                    self.logger.exception(
                        f"Otro tipo de error al conectar {e}, station {self.station}, iteración {counter}")
                    counter += 1
                    await asyncio.sleep(10+counter)
                continue
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                self.logger.exception(
                    f"Excepción por desconexión {conn_error}")
                continue
            except Exception as e:
                msg = f"Excepción no considerada e"
                print(msg)
                self.logger.exception(msg)
                continue
            await asyncio.sleep(10+counter)

        return idc

    # callback for create server:

    async def heart_beat(self, idc):
        tnow = now()
        if idc in self.clients.keys():
            reader = self.clients[idc]['reader']
            writer = self.clients[idc]['writer']
            closing = writer.is_closing()
            extra_info = writer.get_extra_info('peername')
            at_eof = reader.at_eof()
            if not closing and extra_info and not at_eof:
                return True
            else:
                msg_error = f"Closing {closing}, extra_info {extra_info}, at_eof {at_eof}"
                print(msg_error)
                self.logger.error(msg_error)
                self.logger.error(f"no heart_beat, at {tnow}")
                try:
                    await wait_for(self.close(idc), timeout=10)
                except asyncio.TimeoutError as te:
                    self.logger.exception(
                        f"Tiempo fuera en intento de cerrar conexión {te}, station {self.station}")
                    await asyncio.sleep(10)
                except asyncio.IncompletereadError as e:
                    self.logger.exception(
                        f"Excepción por lectura incomplete  {e}, station {self.station}")
                    await asyncio.sleep(10)
                except asyncio.CanceledError as e:
                    self.logger.exception(
                        "Excepción por error de cancelación  {e}, station {self.station}")
                    await asyncio.sleep(10)
                except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                    self.logger.exception(
                        "Excepción por desconexión {conn_error}, station {self.station}")
                    await asyncio.sleep(10)
                except Exception as e:
                    print(f"Excepción no considerada, {e}")
                    self.logger.exception(
                        f"Excepción no considerada {e}, station {self.station}")
                    await asyncio.sleep(10)
                self.logger.exception(
                    "Cerrando correctamente la conexión, por no heartbeat")
                self.status = False
                return False
        else:
            self.logger.error(
                "no heart_beat, idc %s not client, code station %s" % (idc, self.station))
            await self.close(idc)
            self.status = False
            return False

    def info(self, idc):
        if self.clients:
            writer = self.clients[idc]['writer']
            return idc, writer.get_extra_info('peername')
        else:
            return idc, None

    def set_idc(self):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        uin = 4
        idc = my_random_string(uin)
        while True:
            if idc not in self.idc:
                self.idc.append(idc)
                break
            else:
                idc = my_random_string(uin)
        return idc

    async def set_reader_writer(self, reader, writer):
        idc = self.set_idc()
        # self.log_info_client(writer)
        self.clients.update(
            {idc: {
                'reader': reader,
                'writer': writer
            }
            }
        )
        return idc

    def list_clients(self):
        for i in range(len(self.conss)):
            print(str(self.addrs[i]) + ":" + str(self.conns[i]))

    async def close(self, idc):
        self.logger.error("La conexión se cerró en cliente %s" % idc)
        self.status = False
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        writer.close()
        try:
            await wait_for(writer.wait_closed(), timeout=10)
        except asyncio.TimeoutError as te:
            print(f"Close->Error Timeout al leer {te} bytes en {self.station}")
            self.logger.exception(
                f"Station {self.station}, Tiempo fuera al leer en readbytes, {te}")
        except asyncio.IncompleteReadError as ir:
            print("Close_>Incomplete read, station {self.station}")
            self.logger.exception(
                f"Station {self.station}, Tiempo fuera al no poder leer en close, {ir}")
        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
            self.logger.exception(
                f"Close->Excepción por desconexión al intentar leer {conn_error}")
        except Exception as e:
            print("Excepción no considerada")
            self.logger.exception(
                f"Close->Excepción no considerada al intentar leer e")

    async def stop(self):
        for idc in self.clients:
            await self.close(idc)

    async def readbytes(self, reader, n):
        future = reader.readexactly(n)
        try:
            timeout = self.timeout
            if n > 1:
                timeout = timeout*n
            result = await wait_for(future, timeout=timeout)
            return result
        except BrokenPipeError as be:
            print("readbytes", f"Error broken pip {be}")
            return b''
        except asyncio.IncompleteReadError as ir:
            print(
                f"Error por lectura incomplete al leer {n} bytes en {self.station}")
            self.logger.exception(
                f"Station {self.station}, lectura incomplete al leer en readbytes, error: {ir}")
        except asyncio.TimeoutError as te:
            print(f"Error Timeout al leer {n} bytes en {self.station}")
            self.logger.exception(
                f"Station {self.station}, Tiempo fuera al leer en readbytes, {te}")
            if self.raise_timeout:
                raise te
            else:
                return b''
        except asyncio.IncompleteReadError as ir:
            print(f"Incomplete read, station {self.station}")
            self.logger.exception(
                f"Station {self.station}, Tiempo fuera al no poder leer en readbytes {n} bytes, {ir}")
            return b''
        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
            self.logger.exception(
                f"Excepción por desconexión al intentar leer {conn_error}")
            return b''
        except Exception as e:
            print("Excepción no considerada")
            self.logger.exception(
                "Excepción no considerada al intentar leer {e}")
            return b''

    async def get_message_header(self, idc):
        self.idc = idc

    async def get_records(self):
        """
        Esta corutina toma los datos en bytes y los transforma,
        debe entregar una verificaciond e checksum y un diccionario
        """
        return False, {}
