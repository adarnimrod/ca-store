import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')
parametrize = pytest.mark.parametrize


def test_ssl_cert_group(Group):
    assert Group('ssl-cert').exists


@parametrize('directory', ['/usr/share/ca-certificates',
                           '/usr/local/share/ca-certificates',
                           '/etc/ssl/certs'])
def test_cert_directory(File, directory):
    assert File(directory).is_directory


def test_key_directory(File):
    directory = File('/etc/ssl/private')
    assert directory.is_directory
    assert directory.user == 'root'
    assert directory.group == 'ssl-cert'
    assert directory.mode == 0o0710


def test_concat_cert(File, Command):
    assert File('/etc/ssl/certs/ca-certificates.crt').is_file
    assert Command('grep BEGIN /etc/ssl/cert.pem | wc -l').stdout == Command(
        'grep BEGIN /usr/share/ca-certificates/*.crt | wc -l').stdout


def test_update_ca_certificates(File, SystemInfo, Command, Sudo):
    if SystemInfo.type == 'openbsd':
        filename = '/usr/local/sbin/update-ca-certificates'
    elif SystemInfo.type == 'linux' and SystemInfo.distribution in ['debian',
                                                                    'ubuntu']:
        filename = '/usr/sbin/update-ca-certificates'
    update_ca_certificates = File(filename)
    assert update_ca_certificates.is_file
    assert update_ca_certificates.mode == 0o0755
    with Sudo():
        assert Command(filename).rc == 0


def test_snakeoil_cert(File):
    assert File('/etc/ssl/certs/ssl-cert-snakeoil.pem').is_file


def test_snakeoil_key(File, Sudo):
    snakeoil_key = File('/etc/ssl/private/ssl-cert-snakeoil.key')
    with Sudo():
        assert snakeoil_key.is_file
        assert snakeoil_key.group == 'ssl-cert'
        assert snakeoil_key.mode == 0o0640
