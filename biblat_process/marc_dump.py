#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import datetime
import logging
import os
import subprocess

from biblat_process.utils import CustomFormatter
from biblat_process.settings import config

logger = logging.getLogger('claper_dump')
custom_formatter = CustomFormatter()

UNTIL = datetime.datetime.now().strftime('%Y%m01')
LOGGER_FMT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'


class Dumper:

    def __init__(self, until_date=UNTIL):
        self.date = datetime.datetime.now().strftime('%d%m%y')
        self.limit_date = until_date
        self.user_host = '{user}@{host}'.format(user=config.REMOTE_USER,
                                                host=config.REMOTE_ADDR)

    def list_claper(self, base):
        logger.info('Generando listado de %s' % base.upper())
        script = "set source_par = '{dlib}'\n" \
                 "source ${{alephm_proc}}/set_lib_env\n" \
                 "setenv PATH /exlibris/aleph/.local/bin:$PATH\n" \
                 "set fentrada=sis{dlib}_{fecha}.lst\n" \
                 "sqlplus {dlib}/{dlib} @/dev/stdin <<EOF\n" \
                 "SET HEADING ON\n" \
                 "SET LINESIZE 14\n" \
                 "SET ECHO OFF\n" \
                 "SET FEEDBACK OFF\n" \
                 "SET PAUSE OFF\n" \
                 "SET NEWPAGE 0\n" \
                 "SET SPACE 0\n" \
                 "SET PAGESIZE 0\n" \
                 "SET TERMOUT OFF\n" \
                 "SET VERIFY OFF\n" \
                 "SPOOL $alephe_scratch/$fentrada\n" \
                 "SELECT SUBSTR(Z13u_REC_KEY, 1, 9)||'{dlib!u}' " \
                 "FROM {dlib!u}.Z13u INNER JOIN {dlib!u}.Z13 " \
                 "ON (z13u_rec_key=z13_rec_key) " \
                 "WHERE z13u_user_defined_3_code IS NULL " \
                 "AND z13_upd_time_stamp < '{limit_date}' " \
                 "ORDER BY SUBSTR(z13u_rec_key, 1, 9);\n" \
                 "SPOOL OFF\n" \
                 "EXIT\n" \
                 "EOF\n"

        if base == 'per01':
            script += "gsed -i '/^000200053/d' $alephe_scratch/$fentrada\n"

        script = custom_formatter.format(script,
                                         dlib=base,
                                         limit_date=self.limit_date,
                                         fecha=self.date)

        ssh = subprocess.Popen(["ssh", self.user_host, "csh -s"],
                               shell=False,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        ssh.communicate(script.encode())
        ssh.wait()
        logger.info('Listado de %s generado' % base.upper())

    def dump_claper(self, base):
        logger.info('Generando respaldo de %s' % base.upper())
        script = "set source_par = '{dlib}'\n" \
                 "source ${{alephm_proc}}/set_lib_env\n" \
                 "set fentrada=sis{dlib}_{fecha}.lst\n" \
                 "set fsalida={dlib}json_{fecha}.txt\n" \
                 "cd {remote_path}\n" \
                 "rm -rf $fsalida\n" \
                 "csh -f $aleph_proc/p_print_03 {dlib!u},$fentrada,ALL,,,,,,,,$fsalida,A,,,,N\n" \
                 "echo 'EOF' >> $data_scratch/$fsalida\n" \
                 "echo `wc -l $alephe_scratch/$fentrada | awk '{{print $1}}'` >> $data_scratch/$fsalida\n" \
                 "gzip -c $data_scratch/$fsalida > $fsalida.gz\n" \
                 "rm $data_scratch/$fsalida\n"

        script = custom_formatter.format(script,
                                         dlib=base,
                                         remote_path=config.REMOTE_PATH,
                                         fecha=self.date)

        ssh = subprocess.Popen(["ssh", self.user_host, "csh -s"],
                               shell=False,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        ssh.communicate(script.encode())
        ssh.wait()
        logger.info('Respaldo de %s generado' % base.upper())

    def pull_claper(self, base):
        logger.info('Descargando respaldo de %s' % base.upper())
        cmd = "cat {remote_path}/{dlib}json_{fecha}.txt.gz".format(
            remote_path=config.REMOTE_PATH,
            dlib=base,
            fecha=self.date)
        output_file = open('{local_path}/{dlib}.txt.gz'.format(
            local_path=config.LOCAL_PATH, dlib=base), 'w')

        ssh = subprocess.Popen(["ssh", self.user_host, cmd],
                               shell=False,
                               stdout=output_file)
        ssh.wait()
        output_file.close()
        logger.info(
            'Respaldo de %s descargado en %s' %
            (base.upper(), output_file.name)
        )


def main():
    parser = argparse.ArgumentParser(
        description="Cosecha de archivos"
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    parser.add_argument(
        '--until_date',
        '-u',
        default=UNTIL,
        help='Fecha en formato ISO como %s' % UNTIL
    )

    parser.add_argument(
        '--clase',
        action='store_true',
        dest='clase',
        help='Procesar solo CLASE'
    )

    parser.add_argument(
        '--periodica',
        action='store_true',
        dest='periodica',
        help='Procesar solo PERIÓDICA'
    )

    parser.add_argument(
        '--exec',
        '-e',
        default='all',
        choices=['list', 'dump', 'pull', 'all'],
        help='Seleccione proceso a ejecutar'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.logging_level.upper(), 'INFO'),
        format=LOGGER_FMT)

    d = Dumper(until_date=args.until_date)
    bases = ['cla01', 'per01']

    if args.clase:
        bases = ['cla01']

    if args.periodica:
        bases = ['per01']

    for base in bases:
        if args.exec in ('list', 'all'):
            d.list_claper(base)

        if args.exec in ('dump', 'all'):
            d.dump_claper(base)

        if args.exec in ('pull', 'all'):
            d.pull_claper(base)


if __name__ == "__main__":
    main()
