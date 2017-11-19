import datetime
import sys
import json
import subprocess


def _get_ips(obj):
    return map(lambda x: x['Node']['Address'], obj)

def _excute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    print('[{}]'.format(stdout_data.strip()))
    print('[{}]'.format(stderr_data.strip()))
    return stdout_data.strip(), stderr_data.strip()

def get_input_from_consul():
    input_line = sys.stdin.readline()
    obj = json.loads(input_line)
    return obj

def peer_join(obj):
    for ip in _get_ips(obj):
        cmd = 'gluster peer probe {}'.format(ip)
        stdout_data, stderr_data = _excute(cmd)
        if not stdout_data.startswith('peer probe: success.'):
            raise Exception("Peer Probing Error")
        if stderr_data != '':
            raise Exception("StdErr Received")

def volume_list():
    cmd = 'gluster volume list'
    stdout_data, stderr_data = _excute(cmd)
    if stderr_data == 'No volumes present in cluster':
        return []
    return stdout_data.split("\n")

def create_volume(vol_name, vol_mode='replica 3'):
    nodes = [
      "{}:/glusterfs/distributed".format(ip) for ip in _get_ips(obj)
    ]
    cmd = 'gluster volume create {} {} {} force'.format(vol_name, vol_mode, ' '.join(nodes))
    print cmd
    stdout_data, stderr_data = _excute(cmd)
    if stdout_data != 'volume create: {}: success: please start the volume to access data'.format(vol_name):
        raise Exception('Volume Creating Error')


def start_volume(vol_name):
    cmd = 'gluster volume start {}'.format(vol_name)
    print cmd
    stdout_data, stderr_data = _excute(cmd)
    if stdout_data != 'volume start: {}: success'.format(vol_name):
        raise Exception('Volume Starting Error')


def stop_volume(vol_name):
    cmd = 'echo y | gluster volume stop {}'.format(vol_name)
    print cmd
    stdout_data, stderr_data = _excute(cmd)
    tmp = 'Stopping volume will make its data inaccessible. Do you want to continue? (y/n) '
    stdout_data = stdout_data.replace(tmp, '')
    if stdout_data != 'volume stop: {}: success'.format(vol_name):
        raise Exception('Volume Stoping Error')

def delete_volume(vol_name):
    cmd = 'echo y | gluster volume delete {}'.format(vol_name)
    print cmd
    stdout_data, stderr_data = _excute(cmd)
    tmp = 'Deleting volume will erase all information about the volume. Do you want to continue? (y/n) '
    stdout_data = stdout_data.replace(tmp, '')
    if stdout_data != 'volume delete: {}: success'.format(vol_name):
        raise Exception('Volume Deleting Error')


obj = get_input_from_consul()
peer_join(obj)

create_volume('taguro')
#print volume_list()
start_volume('taguro')
#stop_volume('taguro')
#delete_volume('taguro')
