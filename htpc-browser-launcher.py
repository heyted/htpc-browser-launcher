#!/usr/bin/env python3
# Example usage: htpc-browser-launcher.py chromium-browser

import os, sys, dbus, subprocess, shutil, configparser
from shlex import split

if __name__ == '__main__':
    #Read settings:
    config = configparser.RawConfigParser()
    homepath = os.path.expanduser('~')
    if os.path.isfile(homepath + '/.htpc-browser-launcher/htpc-browser-launcher.cfg'):
        config.read(homepath + '/.htpc-browser-launcher/htpc-browser-launcher.cfg')
        use_keynav = config.getboolean('htpc_browser_launcher_settings', 'use_keynav')
        use_unclutter = config.getboolean('htpc_browser_launcher_settings', 'use_unclutter')
        use_no_screensaver = config.getboolean('htpc_browser_launcher_settings', 'use_no_screensaver')
        open_streaming_links_site = config.getboolean('htpc_browser_launcher_settings', 'open_streaming_links_site')
        browser = config.get('htpc_browser_launcher_settings', 'browser')
    else:
        print("Could not find settings file.  Using default settings.")
        use_keynav = True
        use_unclutter = True
        use_no_screensaver = False
        open_streaming_links_site = True
        browser = "chromium-browser"
    #Set browser (command line argument overrides settings file):
    if len(sys.argv) > 1:
        if sys.argv[1] in ["google-chrome", "firefox", "chromium-browser"]:
            browser = sys.argv[1]
    elif browser in ["google-chrome", "firefox", "chromium-browser"]:
        pass
    elif shutil.which("google-chrome"):
        browser = "google-chrome"
    elif shutil.which("firefox"):
        browser = "firefox"
    elif shutil.which("chromium-browser"):
        browser = "chromium-browser"
    else:
        print("HTPC Browser Launcher is only compatible with Chrome, Chromium and Firefox.  Exiting.")
        sys.exit(0)
    #Inhibit screensaver and screen blanking while browser is open:
    if use_no_screensaver:
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.freedesktop.ScreenSaver','/org/freedesktop/ScreenSaver')
        iface = dbus.Interface(proxy, 'org.freedesktop.ScreenSaver')
        cookie = iface.Inhibit(browser, "gnome-inhibit")
    #Start keynav:
    if use_keynav:
        if shutil.which("keynav"):
            subprocess.run("keynav", shell=False)
        else:
            print("Keynav not installed.  Not starting Keynav.")
            use_keynav = False
    #Start unclutter:
    if use_unclutter:
        if shutil.which("unclutter"):
            subprocess.Popen("unclutter", shell=False)
        else:
            print("Unclutter not installed.  Not starting Unclutter.")
            use_unclutter = False
    #Start browser:
    if browser == "firefox":
        fullscreenmethod = " --kiosk"
    else:
        fullscreenmethod = " --start-fullscreen"
    if open_streaming_links_site:
        command = split(browser + fullscreenmethod + ' https://lv.tedsblog.org')
    else:
        command = split(browser + fullscreenmethod)
    try:
        subprocess.run(command, shell=False)
    except FileNotFoundError:
        print('Command not recognized: ' + browser)
        if not shutil.which(browser):
            print("It appears the browser is not installed")
        print('Aborting')
    #Stop keynav:
    if use_keynav:
        command = split("start-stop-daemon --stop --name keynav")
        subprocess.run(command, shell=False)
    #Stop unclutter:
    if use_unclutter:
        command = split("start-stop-daemon --stop --name unclutter")
        subprocess.run(command, shell=False)
