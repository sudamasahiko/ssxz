# ssxzシステム起動方法  
各マシンへSSH接続し、Agentを起動(以下は二台目の例)  
\# ssh 192.168.122.4  
\# python /home/ssxz/ssxz  
\# python Agent.py 2  
1台目にてWebAPI Serverを起動  
\# cd /home/ssxz/ssxz  
\# python ssxz_daemon.py start  
Data Center Managerを起動  
\# python dcm.py  

# デモンストレーション方法  
1台目にてcurlコマンドを発行  
\# curl 'http://192.168.122.3:8000?cmd=make_vm&cpu=1&ram=1024&disk=4'  
上記コマンド実行後、Web API ServerはリクエストキューにVM作成の要求を投げる。  
DataCenterManagerはリソース管理のDBと照合したのち、タスクキューへVM作成のためのメッセージをエンキューする。  
各Agentはタスクキューから要求をデキューし、VMの作成・削除を行う。  
インストール状況は定期的にポーリングを行い、完了後はリザルトキューにSSH秘密鍵を送信する。  
VMの削除は以下コマンドで可能
\# curl 'http://192.168.122.3:8000?cmd=kill_vm&id=4'  
VMの作成と同様、VMの作成と同様、リクエストキュー、タスクキューを利用し、Agent経由でVMの削除が行われる。  

# ssxz作業手順書  
  
1.OpenSSHがインストールされているか確認 -> OK。CentOSはデフォルトでインストール済み。  
/usr/sbin/sshd --help  
  
2.一般ユーザにてSSHの鍵ペアを作成  
cd ~/.ssh  
上記なければmkdir ~/.ssh  
chmod 700 ~/.ssh  
ssh-keygen -t rsa  
pass phraseは以下を設定  
1234qwer  
cat id_rsa.pub >> authorized_keys  
chmod 600 authorized_keys  
  
3.sshdの設定  
\# vi /etc/ssh/sshd_config  
PasswordAuthentication no  
PermitRootLogin no  
PermitEmptyPassword no  
Port 50122  
systemlctl restart sshd.service  
  
3.ポートチェックのツールをインストール  
\# yum install -y nmap  
  
4.ポートの疎通を確認  
\# firewall-cmd --zone=public --query-port=50122/tcp  
no  
firewall-cmd --zone=public --add-port=50122/tcp --permanent  
\# firewall-cmd --zone=public --query-port=50122/tcp  
-> yes -> ok!  
  
5.外部からSSH接続を確認 -> ok!  
puttyを使用(putty用に秘密鍵のフォーマットを変換する必要あり)  
  
6.2～4台目のネットワーク設定を調整。 
以下を設定しました(後程ブリッジ接続へ変更)。  
\# nmcli con mod em1 ipv4.addresses "192.168.0.2/24 192.168.0.1"  
\# nmcli con mod em1 ipv4.method manual  
\# nmcli con mod connection.autoconnect  
\# nmcli con up em1  
\# systemctl restart NetworkManager  
\# ifconfig  
ok!  
  
7.1台目にて以下のユーザを作成しました。  
xu  
zhu  
zhao  
ssxz  
各ユーザにて、ssh用の鍵を格納するディレクトリを作成  
mkdir ~/.ssh  
chmod 700 ~/.ssh  
cd ~/.ssh  
ssh-keygen -t rsa  
cat id_rsa_[username] >> authorized_keys  
chmod 600 authorized_keys
秘密鍵を各ユーザに配布

8.2-4台目にssxzユーザを作成し、SSH設定を行った(パスワード接続)。  
  
9.1台目から2-4台目に疎通を確認(ping, ssh接続)  
  
10.2,3,4台目に以下を実行
【install libvirt】
\# yum install -y qemu-kvm virt-manager libvirt libvirt-python virt-install virt-viewer  
\# systemctl start libvirtd  
\# systemctl enable libvirtd  
  
【install pip】  
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"  
python get-pip.py  
  
【ssh packages for python】  
\# yum install -y gcc libffi-devel python-devel openssl-devel  
\# pip install paramiko  
  
【scp file transfer】  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.2:/home/ssxz  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.3:/home/ssxz  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.4:/home/ssxz  
  
14.全マシンをブリッジ接続に変更  
\# brctl addbr br0  
\# ip link set br0 up  
\# brctl addif br0 em1  
/etc/network-script/ifcfg-br0  
上記にてDNSアドレス、ゲートウェイを設定
  
15.イメージファイルの転送  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.2:/home/ssxz  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.3:/home/ssxz  
scp CentOS-7-x86_64-Minimal-1511.iso root@192.168.0.4:/home/ssxz  
  
16.各マシンへAgent.pyをデプロイ
