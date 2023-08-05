import subprocess
import os

def run(label=''):
    pydir = os.path.dirname(os.path.abspath(__file__)) # mindaffectBCI/decoder/startUtopiaHub.py
    bindir = os.path.join(pydir,'..','..','bin') # ../../bin/

    # make the logs directory if not already there
    try: 
        os.mkdir(os.path.join(bindir,'..','logs'))
    except:
        pass

    # command to run the java hub
    cmd = ("java","-jar","UtopiaServer.jar")
    # args to pass to the java hub
    if label is not None:
        logfile = "../logs/mindaffectBCI_{}.txt".format(label)
    else:
        logfile = "../logs/mindaffectBCI.txt"
    args = ("8400","0",logfile)

    # run the command, waiting until it has finished
    print("Running command: {}".format(cmd+args))
    utopiaHub = subprocess.run(cmd + args, cwd=bindir, shell=False,
                               stdin=subprocess.DEVNULL)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Result: {}".format(utopiaHub.stdout))
    return utopiaHub

if __name__=="__main__":
    run()