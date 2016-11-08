# 
# Vminterface
# by suda (group2)
# lastmod: 2016.11.
# 

import subprocess
import paramiko
import os

class Vminterface():
    """Class: Vminterface

        usage:
            obj = Vminterface('centos7_2', '192.168.122.2')
            obj.make_instance(1, 1024, 4)
    """

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.dir = '/var/kvm/disk/' + name + '/'

    # check if vm is running
    def is_up(self):
        ret = self.fire('virsh domstate ' + self.name, True)
        if ret.find('running') >= 0:
            return True
        else:
            return False

    def is_ssh_up(self):
        if not self.is_up():
            return False
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
              ssh.connect(self.ip, username='root', password='1234qwer', key_filename='/var/kvm/disk/' + self.name + '/id_rsa')
              return True
            except:
              return False
            ssh.close()

    # check if vm is installed
    def has_instance(self):
        ret = self.fire('virsh dominfo ' + self.name + ' | grep UUID:', True)
        if ret.find('UUID:') >= 0:
            return True
        else:
            return False

    def start(self):
        if not self.is_up():
            self.fire('virsh start ' + self.name, True)

    def undefine(self):
        # self.fire('virsh destroy ' + self.name, True)
        # self.fire('virsh undefine ' + self.name, True)
        FNULL = open(os.devnull, 'w')
        cmd = 'virsh destroy ' + self.name
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=FNULL, stderr=FNULL, close_fds=True)
        cmd = 'virsh undefine ' + self.name
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=FNULL, stderr=FNULL, close_fds=True)
        cmd = 'umount -l /var/kvm/disk/' + self.name + '/md_mount'
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=FNULL, stderr=FNULL, close_fds=True)
        cmd = 'rm -rf /var/kvm/disk/' + self.name
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=FNULL, stderr=FNULL, close_fds=True)

    def make_instance(self, cpu, ram, hdd):
        self.make_dir(self.dir)
        self.pubkey = self.make_ppk()
        self.make_kickstart(self.dir + 'kickstart.cfg')
        self.make_virshcmd(self.name, str(cpu), str(ram), str(hdd), self.dir + 'virshcmd.sh')
        
        # start without output
        # FNULL = open(os.devnull, 'w')
        # cmd = 'sh ' + self.dir + 'virshcmd.sh'
        # subprocess.call(cmd.strip().split(" "), stdout=FNULL, stderr=subprocess.STDOUT)
        FNULL = open(os.devnull, 'w')
        cmd = 'sh ' + self.dir + 'virshcmd.sh'
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=FNULL, stderr=FNULL, close_fds=True)

    def fire(self, cmd, no_out=False):
        FNULL = open(os.devnull, 'w')
        # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=FNULL, shell=True)
        proc_stdout = process.communicate()[0].strip()
        if not no_out:
            print proc_stdout
        return proc_stdout

    def make_ppk(self):
        self.fire('ssh-keygen -q -t rsa -f ' + self.dir + 'id_rsa -N 1234qwer')
        with open(self.dir + 'id_rsa.pub') as myfile:
            return myfile.read().replace('\n', '')

    def make_dir(self, dir):
        self.fire('mkdir ' + dir + ';')

    def make_kickstart(self, filename):
        output = """#version=DEVEL
# System authorization information
auth --enableshadow --passalgo=sha512
cdrom
text
firstboot --enable
ignoredisk --only-use=vda
skipx
lang en_US.UTF-8
keyboard --vckeymap=jp106 --xlayouts=jp
network --hostname=""" + self.name + """
rootpw --plaintext 1234qwer
selinux --disabled
#firewall --disabled
timezone --utc Asia/Tokyo
user --name=ssxz --password=1234qwer

# System bootloader configuration
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=vda
autopart --type=lvm

# Partition clearing information
clearpart --all --initlabel --drives=vda

reboot

%packages
@core
kexec-tools

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end

%post
#!/bin/sh

#mkdir /metadata
#mount LABEL=METADATA /metadata
#sh /metadata/bootscript

chmod +x /etc/rc.d/rc.local

echo "#!/bin/sh" >> /bootscript
echo "sh /bootscript" >> /etc/rc.d/rc.local
echo "hostnamectl set-hostname """ + self.name + """\" >> /bootscript
echo "nmcli con mod eth0 ipv4.addresses """ + self.ip + """/24" >> /bootscript
echo "nmcli con mod eth0 ipv4.method manual" >> /bootscript
echo "systemctl restart NetworkManager" >> /bootscript
echo "systemctl restart network" >> /bootscript
echo "mkdir /root/.ssh" >> /bootscript
echo "chmod 700 /root/.ssh" >> /bootscript
echo "echo \"""" + self.pubkey + """\" >> /root/.ssh/authorized_keys" >> /bootscript
echo "chmod 600 /root/.ssh/authorized_keys" >> /bootscript

%end
"""
        f = open(filename, 'w')
        f.write(output)
        f.close()

    def make_virshcmd(self, name, cpu, ram, hdd, filename):
        #--disk path=/var/kvm/disk/""" + name + """/metadata_drive,device=disk,format=vfat \\
        output = """virt-install \\
--name=""" + name + """ \\
--vcpus=""" + cpu + """ \\
--ram=""" + ram + """ \\
--location=/home/ssxz/CentOS-7-x86_64-Minimal-1511.iso \\
--disk path=/var/kvm/disk/""" + name + """/disk.qcow2,format=qcow2,size=""" + hdd + """ \\
--network bridge=virbr0 \\
--arch=x86_64 \\
--os-type=linux \\
--os-variant=rhel7 \\
--nographics \\
--initrd-inject /var/kvm/disk/""" + name + """/kickstart.cfg \\
-v -x \"inst.ks=file:/kickstart.cfg console=ttyS0\"
"""
        f = open(filename, 'w')
        f.write(output)
        f.close()