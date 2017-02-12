import requests
import os
import errno


def set_wallpaper(wp_uri):
    # TODO: set wallpaper for different OS
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://" + wp_uri)


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


if __name__ == '__main__':
    change_wallpaper()
