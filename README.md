## _AUTO TX BANYAK WALLET KE BANYAK ADDRESS (MANY TO MANY)_

## Installation


```sh
pip install aiohttp pynacl
git clone https://github.com/kenjisubagja/octra-auto
cd octra-auto
```

edit dulu wallets.txt dengan adress dan pk kelean
```sh
oct4xxx1|||base64key1
oct4xxx2|||base64key2
oct4xxx3|||base64key3
oct4xxx4|||base64key4
oct4xxx5|||base64key5
```
dan edit isi p.txt yaitu address yang mau kita send/penerima 
```sh
oct4xxx1
oct4xxx2
oct4xxx3
oct4xxx4
oct4xxx5
```
## cara run pake python3 atau python
```sh
python3 multi.py
```
exploler octra : https://octrascan.io/
# Cek tx multi address #
https://octra-check-tx.vercel.app/

### Note : jika di vps pas ```install pip install aiohttp pynacl``` atau error pas run ```python3 multi.py``` pake cara ini 
jika banyak wallet dan tx banyak pastikan membuat screen terlebih dahulu

```sh
sudo apt install python3-venv
```
```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
```
```sh
pip install aiohttp pynacl
```
```sh
python3 multi.py
```
## Bang Kenji subagja ganteng 😆 ##
