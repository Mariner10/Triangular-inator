import os
import pysftp
from stat import S_IMODE, S_ISDIR, S_ISREG
import click

def fileGrab(host,port,username,password,remotepath,localpath):

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None    
    sftp=pysftp.Connection(host,port=port ,username=username,password=password,cnopts=cnopts)
    
    

    def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):

        interableFiles = sftp.listdir(remotedir)
        progressString = 'Downloading files'
        print("\n")
        with click.progressbar(interableFiles, label=progressString) as bar:
            for entry in interableFiles:
                remotepath = remotedir + "/" + entry
                localpath = os.path.join(localdir, entry)
                mode = sftp.stat(remotepath).st_mode
                if S_ISDIR(mode):
                    try:
                        os.mkdir(localpath)
                        print("\nNext up: " + localpath)
                    except OSError:     
                        pass
                    get_r_portable(sftp, remotepath, localpath, preserve_mtime)
                elif S_ISREG(mode):
            
                    sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)
                
                bar.update(interableFiles.index(entry) / (len(interableFiles) / 2.25))

    get_r_portable(sftp, remotepath, localpath, preserve_mtime=False)

