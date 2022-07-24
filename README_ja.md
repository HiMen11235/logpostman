#　logpostmanについて
logpostmanは
# Requirements
```
Python3.x
scapy=2.4.5
```
# Installation
Githubのページからリポジトリを任意のローカル環境にクローンしてください。
# Usage
sudo または root 権限で、以下を実行します。
```
python3 logpostman.py host -f /file/to/path
```
 を実行してください。実行すると、hostの部分で指定されたIPアドレスを宛先IPアドレスとして、ファイルに含まれるデータを継続的にホストに送ります。(デフォルト: 1000events/s)
送信元の IP アドレスを任意の IP アドレスとして送信する場合は、
```
python3 logpostman.py host -a yy.yy.yy.yy -f/file/to/path
```
と、-aオプションを付加します。します。
基本的な使い方は上記の通りですが、その他のオプションについては、-h,--help で表示されるヘルプ情報を確認してください。
# License
GPLv2
