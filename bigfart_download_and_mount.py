import traceback
from ftplib import FTP
import sys

global PORT
PORT = 2121

global HOST
HOST = '1.1.1.2'

global savenum
savenum = '0'





def ohnoes_errorhappend(theerror):
    try: ftp.close()
    except: pass 
    import winsound
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    input(theerror +'\nyeah an error happend')
    sys.exit()


def ftp_loginANDconnect(HOST, PORT='21'):
    ftp = FTP()
    ftp.connect(HOST, PORT)
    ftp.login()
    return ftp
    
ftp = ftp_loginANDconnect(HOST,PORT)


def list_all_files_in_folder_ftp(ftp,source_folder=''): #gets a list of all the folders and files in a folder (inlcuding subdirs), this one took me a while to make!
    def get_list_LIST(path=source_folder):
        lines = []
        ftp.retrlines('LIST ' +path , lines.append)
        lines.pop(0); lines.pop(0) #ill come up with a cleaner method later, get rid of useless non files
        return lines

    old_mememory = ftp.pwd()
    filesnfolders = []
    ftp.cwd(source_folder)

    def recur_over_folder(list,path=source_folder):
        for file in get_list_LIST(path):
            clean_path = f'{path}/{file.split()[-1]}'
            if clean_path in filesnfolders: continue
            else: filesnfolders.append(clean_path)
            if not file.startswith("-"): #again need a cleaner method, used to detirmine if its a file or folder, if it starts with - then its a file
                ftp.cwd(f'{path}/{file.split()[-1]}')
                recur_over_folder(filesnfolders,f'{path}/{file.split()[-1]}')
    recur_over_folder(filesnfolders)
    ftp.cwd(old_mememory)
    return filesnfolders
def ftpdownload(ftp, FILE, DIR='', DESTINATION_NAME=''): #download a file from ftp, you must define the dir though or just looks in root
    if not DIR == '':
        ftp.cwd(DIR)
    old_mememory = ftp.pwd()
    if DESTINATION_NAME == '':
        ftp.retrbinary("RETR " + FILE ,open(FILE, 'wb').write)
    else:
        ftp.retrbinary("RETR " + FILE ,open(DESTINATION_NAME, 'wb').write)
    ftp.cwd(old_mememory)
def ftpupload(ftp, FILE, DIR='', REAL_NAME=''): #upload file to ftp server, must define a dir though or just looks in root
    if not DIR == '':
        ftp.cwd(DIR)
    old_mememory = ftp.pwd()
    if REAL_NAME == '':
        ftp.storbinary('STOR ' + FILE, open(FILE, 'rb'))
    else:
        ftp.storbinary('STOR ' + FILE, open(REAL_NAME, 'rb'))
    ftp.cwd(old_mememory)

    

global bigfart_ftp_dir
bigfart_ftp_dir = ''


try:
    ftp = ftp_loginANDconnect(HOST,PORT)
    for dirrr in list_all_files_in_folder_ftp(ftp,f"/mnt/sandbox/NPXS20001_000/savedata{savenum}"):
        if dirrr.split("/")[-1].startswith("bigfart"):
            bigfart_ftp_dir = dirrr

    if not bigfart_ftp_dir: ohnoes_errorhappend("not right save mounted, check again!!")
    
    dothedownload = False
    try: user_bigfart = sys.argv[1]
    except IndexError: dothedownload = True
    
    if dothedownload: ftpdownload(ftp,bigfart_ftp_dir,f"/mnt/sandbox/NPXS20001_000/savedata{savenum}",bigfart_ftp_dir.split("/")[-1])
    else: 
        aaa = bigfart_ftp_dir.split('/')# getting the dir, remove the bigfart file at the end
        if not aaa[-1]: aaa.pop(-1); aaa.pop(-1)
        else: aaa.pop(-1)
        ee = '/'.join(aaa)
        ftpupload(ftp,bigfart_ftp_dir.split("/")[-1],ee,user_bigfart)
    ftp.close()
except Exception: ohnoes_errorhappend(traceback.format_exc())