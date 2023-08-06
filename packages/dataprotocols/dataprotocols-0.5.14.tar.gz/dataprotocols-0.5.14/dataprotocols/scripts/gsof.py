from dataprotocols.gsof import Gsof
import asyncio
import functools
import os
import signal
import click
import json
import time
from networktools.ip import validURL


async def run_test(loop, code, host, port, limit=2000, show=True):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    print("Inicializando GSOF con:")
    [print(k, "->", v) for k, v in ginput.items()]
    gsof_test = "gsof_test.json"
    limit_counter = limit
    counter = 0
    print("Conexion a->", ginput)
    gsof = Gsof(**ginput)
    print("GSOF object", gsof)
    idc = await gsof.connect()
    print("IDC->", idc)
    with open(gsof_test, "a+") as gsof_file:
        gsof_file.write("[")
        while counter <= limit_counter:
            try:
                print("Heart beat")
                heartbeat = await gsof.heart_beat(idc)
                print("Heartbeat", heartbeat)
                if heartbeat:
                    print("MSG recv>")
                    await gsof.get_message_header(idc)
                    print("Header msg->", gsof.msg_bytes)
                    done, msg = await gsof.get_records()
                    if done:
                        if show:
                            print("Gsof %s" % code)
                            [print(k, "->", v) for k, v in msg.items()]
                        json.dump(msg, gsof_file, indent=2)
                        gsof_file.write(",\n")
                else:
                    await gsof.close(idc)
                    idc = await gsof.connect()
            except Exception as ex:
                gsof_file.write("]")
                await gsof.close(idc)
                print("Error %s" % ex)
                loop.close()
                raise ex
            except KeyboardInterrupt as ke:
                gsof_file.write("]")
                await gsof.close(idc)
                loop.close()
                print(ke)
                raise ke
            counter += 1
        gsof_file.write("]")
    await gsof.close(idc)


@click.command()
@click.option("--code", default="CODE", help="Código de estación")
@click.option("--host", default="AQUI-VA-LA-URL", help="URL de estación")
@click.option("--port", default=9080, help="Nro de puerto")
@click.option("--limit", default=2000, help="Nro de mensajes")
@click.option("--show/--no-show", default=True, show_default=True,
              type=bool, help="Mostrar cada mensaje")
def run_gsof(code, host, port, limit, show):
    loop = asyncio.get_event_loop()
    try:
        if validURL(host):
            loop.run_until_complete(
                run_test(loop, code, host, port, limit, show))
        else:
            print(
                "Ingresa datos reales para obtener resultados: gsof --help \n Revisa tus parámetros nuevamente")
    except Exception as ex:
        print("Exception %s" % ex)
        loop.call_soon_threadsafe(loop.stop)
        print(ex)
    except KeyboardInterrupt as ke:
        print("Exception %s" % ke)
        loop.call_soon_threadsafe(loop.stop)
        print(ke)
    finally:
        loop.close()


if __name__ == '__main__':
    run_gsof()
