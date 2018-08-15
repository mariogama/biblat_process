#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import string
import datetime
from biblat_process.utils import settings

host = "aleph@"+settings.get(u'app:main', {})['remote_addr']
sqlScript = """
set source_par = '{dlib}'
source ${{alephm_proc}}/set_lib_env
setenv PATH /exlibris/aleph/.local/bin:$PATH
set fecha=`date +%d%m%y`
set dir='"""+settings.get(u'app:main', {})['remote_path']+"""
set fentrada=sis{dlib}_$fecha.lst
cd $dir
cat <<EOF > consulta.sql
SET HEADING ON
SET LINESIZE 14
SET ECHO OFF
SET FEEDBACK OFF
SET PAUSE OFF
SET NEWPAGE 0
SET SPACE 0
SET PAGESIZE 0
SET TERMOUT OFF
SET VERIFY OFF
SPOOL $dir/$fentrada
select substr(z13u_rec_key,1,9)||'{dlib!u}'
from {dlib!u}.z13u
where z13u_user_defined_3_code is NULL
order by substr(z13u_rec_key,1,9);

SPOOL OFF
EXIT
EOF
sqlplus {dlib}/{dlib} @consulta.sql
mv $dir/$fentrada $alephe_scratch/$fentrada
exit
"""

script = """
set source_par = '{dlib}'
source ${{alephm_proc}}/set_lib_env
setenv PATH /exlibris/aleph/.local/bin:$PATH
set fecha=`date +%d%m%y`
set dir='"""+settings.get(u'app:main', {})['remote_path']+"""
set fentrada=sis{dlib}_$fecha.lst
set fsalida={dlib}json_$fecha.txt
cd $dir
rm -rf $fsalida
cd $aleph_proc
csh -f p_print_03 {dlib!u},$fentrada,ALL,,,,,,,,$fsalida,A,,,,N
mv $data_scratch/$fsalida $dir
while ( ! -e $dir/$fsalida )
        echo "no existe $fsalida"
        sleep 1
end
echo "EOF" >> $dir/$fsalida
echo `wc -l $alephe_scratch/$fentrada | awk '{{print $1}}'` >> $dir/$fsalida
cd $dir
gzip -9 $fsalida
"""

DATE = datetime.date.today().strftime('%d%m%y')


class cformatter(string.Formatter):

    def __init__(self):
        super(cformatter, self).__init__()

    def convert_field(self, value, conversion):
        # do any conversion on the resulting object
        if conversion is None:
            return value
        elif conversion == 's':
            return str(value)
        elif conversion == 'r':
            return repr(value)
        elif conversion == 'u':
            return value.upper()
        elif conversion == 'l':
            return value.lower()
        raise ValueError(
            "Unknown conversion specifier {0!s}".format(conversion))


cformatter = cformatter()


def list_claper(base, include_scielo=False):
    lsqlScript = sqlScript
    lsqlScript = cformatter.format(lsqlScript, dlib=base)
    print (lsqlScript)
    ssh = subprocess.Popen(["ssh", host, "csh -s"],
                           shell=False,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    ssh.communicate(lsqlScript)
    ssh.wait()


def dump_claper(base, include_scielo=False):
    list_claper(base, include_scielo)
    lscript = cformatter.format(script, dlib=base)

    print (lscript)

    ssh = subprocess.Popen(["ssh", host, "csh -s"],
                           shell=False,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    ssh.communicate(lscript)
    ssh.wait()

    pull_claper(base)


def pull_claper(base):
    dir = settings.get(u'app:main', {})['remote_path']
    cmd = "cat "+dir+"/{dlib}json_{dump_date}.txt.gz"\
        .format(dlib=base, dump_date=DATE)
    output_file = open(settings.get(u'app:main', {})['local_path'] +
                       '/{dlib}_valid.txt.gz'.format(dlib=base), 'w')

    ssh = subprocess.Popen(["ssh",
                            host, cmd],
                           shell=False,
                           stdout=output_file)
    ssh.wait()
    output_file.close()

dump_claper('cla01')
dump_claper('per01')
