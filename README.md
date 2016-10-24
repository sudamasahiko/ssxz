# ssxz作業手順書

1.OpenSSHがインストールされているか確認 -> OK。CentOSはデフォルトでインストール済み。
/usr/sbin/sshd --help

2.一般ユーザにてSSHの鍵ペアを作成
cd ~/.ssh
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
\# firewall-cmd --zone=external --query-port=50122/tcp
no
firewall-cmd --zone=external --add-port=50122/tcp --permanent
\# firewall-cmd --zone=external --query-port=22/tcp
-> yes -> ok!

5.外部からSSH接続を確認 -> ok!
puttyを使用

6.2～4台目のネットワーク設定を調整。ipconfigで設定したIPアドレスは、再起動したら解除されていました。
以下を設定しました。
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
