#!/usr/bin/env python2
# Author: Nicolai Spohrer <nicolai@xeve.de>
# License: GPL v3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import mechanize
import signal

### START USER CONFIG

CHECK_WIFI_CONNECTION_FIRST = True # whether to try to check connection to correct SSID
TEST_IP="8.8.8.8"
TIMEOUT=4 # Timeout is necessary b/c mechanize function sometimes do not return

### END USER CONFIG


def callback_timeout(signum, frame):
    # when timeout triggers
    raise RuntimeError("Timeout triggered")

def login_captive_portal():
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # setup alarm
    signal.signal(signal.SIGALRM, callback_timeout)
    signal.alarm(TIMEOUT)

    br.open("http://cp.ka-wlan.de/login?target=xml", timeout=TIMEOUT)

    # stop alarm
    signal.alarm(0)

    try:
        br.form = list(br.forms())[0]
    except IndexError:
        print("Error: Could not find form on login page")
        return False

    # setup/stop alarm and submit captive portal form
    signal.alarm(TIMEOUT)
    br.submit()
    signal.alarm(0)

    return True

def ping_google_works():
    if os.system("ping -c 1 {}".format(TEST_IP))==0:
        return True
    else:
        return False

def currently_connected_to_kawlan():
    active_connections = os.popen("nmcli -t -f NAME connection show --active").read()
    if "KA-WLAN" in active_connections:
        return True
    else:
        return False

if __name__ == "__main__":
    print("--- pykawlan ---")
    print("This application is not officially made by anyone affiliated with KA-WLAN and might stop working at "
          "any time. By using KA-WLAN you accept "
          "their conditions of use: http://www.ka-wlan.de/nutzungsbedingungen.html")

    if CHECK_WIFI_CONNECTION_FIRST:
        if not currently_connected_to_kawlan():
            print("Apparently not connected to KA-WLAN network. Aborting.")
            exit(1)

    print("-- Trying to login at KA-WLAN captive portal...")
    try:
        login_captive_portal()
    except RuntimeError:
        pass # timeout might not mean it did not work


    if ping_google_works():
        print("Pinging {} successful".format(TEST_IP))
        exit(0)
    else:
        print("Pinging {} failed".format(TEST_IP))
        exit(1)