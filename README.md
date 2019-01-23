# pykawlan
Automatically sign in to KA-WLAN network under Linux

This script checks whether a computer is connected to the [KA-WLAN](https://www.ka-wlan.de/) network of Karlsruhe, Germany, and - if yes - automatically accepts the terms of use so the internet connection is established without user interaction. The author is *not affiliated with KA-WLAN* in any way.  

# Setup
1. Install dependencies
```bash
# on Debian/Ubuntu etc.
sudo apt install python-mechanize
# if package is not available
sudo pip install mechanize
```
2. Download script
```bash
cd /tmp
git clone https://github.com/nspo/pykawlan.git
```
3. Make script accessible
```bash
cd pykawlan
chmod +x pykawlan.py
sudo cp pykawlan.py /usr/local/bin/
```
4. If you want it to automatically execute when NetworkManager connects to a network:
```bash
cd /etc/NetworkManager/dispatcher.d/
sudo ln -s /usr/local/bin/pykawlan.py 02pykawlan
```

# Notes
- You can turn off the check whether the computer is connected to KA-WLAN. This might be a problem if nmcli is not available.
- `mechanize` is not available for Python 3, so Python 2 was used
- Q: *Why would you use KA-WLAN if you could use KA-sWLAN instead without captive portal?* - A: No account needed and sometimes one tends to be more stable than the other.
