from fadetop_bing_wallpaper import ROOT_DIR
from multiprocessing import Process
import os
import sys


start_program = '"{}" "{}"'.format(
    sys.executable,
    os.path.join(ROOT_DIR, 'FadeTopBing', 'fadetop_bing_wallpaper.py')
    )

with open(os.path.join(ROOT_DIR, 'FadeTopBing', 'start.bat'), 'w') as f:
    f.write(start_program)

with open(os.path.join(ROOT_DIR, 'start.vbs'), 'w') as f:
    f.write('''
    set ws=WScript.CreateObject("WScript.Shell")
    ws.Run """{}""",0
    '''.format(os.path.join(ROOT_DIR, 'FadeTopBing', 'start.bat')))

start_fadetop_bing = '"{}"'.format(os.path.join(ROOT_DIR, 'start.vbs'))
os.system(start_fadetop_bing)


os.system('SCHTASKS /Create /F /SC ONLOGON /TN "Fadetop Bing logon" /TR {} /DELAY 5:00'.format(start_fadetop_bing))
os.system('SCHTASKS /Create /F /SC HOURLY /TN "Fadetop Bing hourly" /TR {} /ST 15:00 /ET 19:00'.format(start_fadetop_bing))
