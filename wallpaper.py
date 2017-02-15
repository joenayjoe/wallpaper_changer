#!/usr/bin/env python3
import requests
import os
import errno
import platform

KEEP_RECENT = 5


def get_platform():
    return platform.platform()
"""
This function will clean up the Wallpaper folder to save disk space.
If all wallpapers are removed from the folder, only primary monitor will
show the wallpaper. For external monitor, we need to keep the wallpaper in
Wallpaper folder. So we will keep most KEEP_RECENT number of wallpaper in the folder.
"""


def clean_wallpaper_folder(file_path):
    folder_dir = os.path.dirname(file_path)
    os.system("cd " + folder_dir + " && ls -t | tail -n +" + str(KEEP_RECENT) + " | xargs rm --")


def set_wallpaper(wp_uri):
    # TODO: set wallpaper for different OS
    os_platform = get_platform()
    if os_platform.startswith("Linux"):
        # handle for linux
        os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://" + wp_uri)
    elif os_platform.startswith("Darwin"):
        # handle for MAC
        os.system("osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + wp_uri +"\"'")

    elif os_platform.startswith("Window"):
        # handle for Window
        import ctypes
        SPI_SETDESKWALLPAPER = 20
        r = ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, wp_uri, 3)
        if not r:
            print(ctypes.WinError())

    else:
        print("Your OS is not supported yet.")


def get_bing_wallpaper_of_the_day():
    json_res = requests.get('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')
    return json_res.json()


def change_wallpaper():
    wp_obj = get_bing_wallpaper_of_the_day()

    image_url = 'http://www.bing.com/' + wp_obj['images'][0]['url']
    get_image = requests.get(image_url)

    pic_directory = os.path.expanduser("~/Pictures")
    file_name = pic_directory + "/Wallpapers/" + wp_obj['images'][0]['startdate'] + "_" + wp_obj['images'][0][
        'enddate'] + ".jpg"

    # download wallpaper only if its not downloaded already.
    if not os.path.isfile(file_name):
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(file_name, 'wb') as f:
            for chunk in get_image.iter_content():
                f.write(chunk)

    # set the wallpaper
    set_wallpaper(file_name)
    if not get_platform().startswith("Window"):
        clean_wallpaper_folder(file_name)


if __name__ == '__main__':
    change_wallpaper()
