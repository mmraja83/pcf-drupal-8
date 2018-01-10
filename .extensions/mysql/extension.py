"""MySQL Extension

Downloads, installs and configures MySQL
"""
import os
import os.path
import logging
from build_pack_utils import utils


_log = logging.getLogger('mysql')


DEFAULTS = utils.FormattedDict({
    'MYSQL_VERSION': '5.7.20',
    'MYSQL_HASH': 'db00cba80e9d2957ac3fd026a4eb721f-5',
    'MYSQL_PACKAGE': 'pcf-mysql-client.tar.gz',
    'MYSQL_URL': 'https://s3.eu-central-1.amazonaws.com/pcf-binary/mysql/{MYSQL_PACKAGE}'
})


# Extension Methods
def preprocess_commands(ctx):
    commands = [
        [ 'echo "PATH variable..."'],
        [ 'echo "export PATH=$PATH:/home/vcap/app/php/bin:/home/vcap/app/mysql/bin" > /home/vcap/.bash_aliases']
    ]
    return commands



def service_commands(ctx):
    return {}


def service_environment(ctx):
    return {}

def compile(install):
    print 'Installing MySQL Client %s' % DEFAULTS['MYSQL_VERSION']
    ctx = install.builder._ctx
    inst = install._installer
    workDir = os.path.join(ctx['TMPDIR'], 'mysql')
    inst.install_binary_direct(
        DEFAULTS['MYSQL_URL'],
        DEFAULTS['MYSQL_HASH'],
        workDir,
        fileName=DEFAULTS['MYSQL_PACKAGE'],
        strip=True)
    (install.builder
        .move()
        .everything()
        .under('{BUILD_DIR}/mysql')
        .into(workDir)
        .done())
    (install.builder
        .move()
        .everything()
        .under(workDir)
        .into('{BUILD_DIR}/mysql')
        .done())
    return 0
