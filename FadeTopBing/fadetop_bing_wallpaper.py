# -*- coding: utf-8 -*-
import datetime
import re
import os
import time
import ssl
ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

try:
    from urllib.request import Request
except ImportError:
    from urllib2 import Request


def urlopen(req):
    try:
        from urllib.request import urlopen as f
        return f(req, context=ssl._create_unverified_context())
    except:
        from urllib2 import urlopen as f
        return f(req)


def urlretrieve(url, path):
    try:
        from urllib.request import urlretrieve as f
        return f(url, path)
    except:
        with open(path, 'wb') as f:
            f.write(urlopen(url).read())


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def get_config():
    config_file_path = os.path.join(ROOT_DIR, 'config.txt')
    motto = '请在config.txt文件中配置'
    if os.path.exists(config_file_path):
        with open(config_file_path, 'rb') as m:
            motto = m.read().decode('utf8')
    else:
        with open(config_file_path, 'wb') as m:
            m.write(motto.encode('utf8'))
    return motto


def change_wallpaper(motto, image_path):
    setting_xml_path = os.path.join(ROOT_DIR, 'FadeTop', 'Settings.xml')
    setting_xml_str = r'''
<?xml version="1.0" encoding="UTF-8" ?>
<FadeTopSettings version="3.0" xmlns="http://www.fadetop.com/fadetop/xmlns/settings">
    <States>
        <Application debut="0" auto_fade_enabled="1" />
        <User break_trail="0:0" />
    </States>
    <Options>
        <General activity_timeout="15" idle_timeout="5" fade_again_delay="1" auto_block_enabled="1" />
        <Fader max_opacity="100">
            <Foreground fg_color="#FFFFFF" fg_position="center" fg_offset_x="0" fg_offset_y="0" fg_time_format="auto" fg_message="请在config.txt文件中配置" />
            <Background bg_color="#008040" bg_image_enabled="1" bg_random_image_enabled="0" bg_image_file="" bg_image_position="fill" />
        </Fader>
        <Sound sound_enabled="0" sound_file="" sound_fadein_enabled="0" sound_fadeout_enabled="1" sound_volume_default="50" />
    </Options>
</FadeTopSettings>
    '''
    if not os.path.exists(setting_xml_path):
        with open(setting_xml_path, 'wb') as f:
            f.write(setting_xml_str.encode('utf8'))    

    with open(setting_xml_path, 'rb') as f:
        setting_xml_str = f.read().decode('utf8')
        if not setting_xml_str:
            return
        setting_xml_str = setting_xml_str.replace(
            re.search('(bg_image_file=".*?")', setting_xml_str).group(),
            'bg_image_file="{}"'.format(image_path)
        ).replace(
            re.search('(bg_image_enabled=".*?")', setting_xml_str).group(),
            'bg_image_enabled="1"'
        ).replace(
            re.search('(<Foreground.*?fg_message.*?/>)',
                      setting_xml_str).group(),
            '<Foreground fg_color="#FFFFFF" fg_position="center" fg_offset_x="0" fg_offset_y="0" fg_time_format="auto" fg_message="{}" />'.format(
                motto)
        )
    with open(setting_xml_path, 'wb') as f:
        f.write(setting_xml_str.encode('utf8'))


def kill_process_by_name(process_name):
    for i in os.popen('tasklist').read().split('\n'):
        if process_name in i:
            os.system('taskkill /F /PID {}'.format(i.split()[1]))

def kill_FadeTop():
    kill_process_by_name('FadeTop.exe')

def start_FadeTop():
    os.system('"{}"'.format(os.path.join(ROOT_DIR, 'FadeTop','FadeTop.exe')))


def get_bing_image():
    image_path = get_dynamic_bing_image()
    if image_path:
        return image_path
    url = 'https://cn.bing.com'
    req = Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    content = urlopen(req).read()
    image_name = re.search('<link id="bgLink".*?href="/th\?id=(.*?\.jpg).*?".*?>',
                           str(content),
                           re.S
                           ).groups()[0]
    image_path = os.path.join(ROOT_DIR, 'FadeTopBing', 'fadetop_wallpaper.jpg')
    urlretrieve(url+'/th?id='+image_name, image_path)
    return image_path


def get_dynamic_bing_image():
    tmp_path = os.path.join(
        os.environ['USERPROFILE'], 'AppData', 'Local', 'Packages')
    dy_path = [i for i in os.listdir(tmp_path) if 'DynamicTheme' in i]
    if not dy_path:
        return
    dy_path = dy_path[0]
    dynamic_theme_path = os.path.join(
        tmp_path,
        dy_path,
        'LocalState', 'Bing'
    )
    if not os.path.isdir(dynamic_theme_path):
        return None
    return os.path.join(
        dynamic_theme_path, os.listdir(dynamic_theme_path)[-1])


def run():
    motto = get_config()
    kill_FadeTop()
    change_wallpaper(motto, get_bing_image())
    start_FadeTop()
    

if __name__ == "__main__":
    run()