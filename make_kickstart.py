def make_kickstart():
    output = """
#version=DEVEL
# System authorization information
auth --enableshadow --passalgo=sha512
cdrom
text
firstboot --enable
ignoredisk --only-use=vda
skipx
lang en_US.UTF-8
keyboard --vckeymap=jp106 --xlayouts=jp
network  --bootproto=dhcp --device=eth0 --onboot=on --noipv6
network  --hostname=localhost.localdomain
rootpw --plaintext 1234qwer
#selinux --disabled
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
mkdir /metadata
mount LABEL=METADATA /metadata
sh /metadata/bootscript
#umount /metadata
#mount LABEL=METADATA /metadata
#chmod +x /etc/rc.d/rc.local
#touch /root/bootscript.sh
#chmod +x /root/bootscript.sh
#echo "mount LABEL=METADATA /metadata" >> /root/bootscript.sh
#echo "/root/bootscript.sh" >> /etc/rc.d/tc.local
#reboot
%end
"""

    filename = 'kickstart.cfg'
    f = open(filename, 'w')
    f.write(output)
    f.close()

make_kickstart()
