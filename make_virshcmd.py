def make_virshcmd(name, cpu, ram, hdd):
    output = """virt-install \\
--name=""" + name + """ \\
--vcpus=""" + cpu + """ \\
--ram=""" + ram + """ \\
--location=/home/ssxz/CentOS-7-x86_64-Minimal-1511.iso \\
--disk path=/var/kvm/disk/""" + name + """/disk.qcow2,format=qcow2,size=""" + hdd + """ \\
--disk path=/var/kvm/disk/""" + name + """/metadata_drive,format=vfat \\
--network bridge=virbr0 \\
--arch=x86_64 \\
--os-type=linux \\
--os-variant=rhel7 \\
--nographics \\
--initrd-inject /var/kvm/disk/""" + name + """/kickstart.cfg \\
-v -x \"inst.ks=file:/kickstart.cfg console=ttyS0\"
"""
    filename = 'virshcmd.sh'
    f = open(filename, 'w')
    f.write(output)
    f.close()

make_virshcmd('centos7', 1, 1024, 8)
