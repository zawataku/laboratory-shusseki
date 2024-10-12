# laboratory-shusseki
大学研究室用の出席管理アプリ

## How to use
### Windowsユーザー

NFCカードリーダ用のドライバーをインストールする必要があります．

1. https://zadig.akeo.ie から最新のZadigをDLします．
2. RC-S380をPCに接続します． 
3. Zadigを実行します．
4. Options -> List All Devicesを選択します．
5. 一覧からSONY RC-S380を選択します．
6. "WinUSB Driver"を選択しインストールします．

次にlibusbをインストールします．

1. https://libusb.info からlibusbをダウンロードします．(Downloads -> Latest Windows Binaries)
2. DLしたフォルダを解凍します．
3. `MinGW64\dll\libusb-1.0.dll`を`C:\Windows\System32`にコピーします．
4. `MinGW32\dll\libusb-1.0.dll`を`C:\Windows\SysWOW64`にコピーします．