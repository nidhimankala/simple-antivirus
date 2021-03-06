import os
import sys
from threading import Thread
import subprocess
from time import sleep
import array
import utility
from config import docker_commands


def check_stats(image_name,logpath):
    sleep(2)
    s=""
    print("Scanning file for resource usage....")
    for i in range(2):
        output = subprocess.check_output(docker_commands['stats_image'], shell=True)
        s = array.array('b',output).tostring().decode('utf-8')
        sleep(1)
    os.system(docker_commands['stop_image'])
    utility.process_output(s,logpath)

def generate_docker_file(executable_path):
    exe_path,exe_name= os.path.split(executable_path)
    dockfilepath=exe_path+"/"+"Dockerfile"
    with open(dockfilepath,'w+') as dockfile:
        dockfile.write("FROM java:8")
        dockfile.write("\n")
        dockfile.write("WORKDIR /")
        dockfile.write("\n")
        dockfile.write("ADD "+exe_name+" "+exe_name)
        dockfile.write("\n")
        dockfile.write("EXPOSE 8080")
        dockfile.write("\n")
        cmd_string="["
        cmd_list=[]
        dockfile.write("CMD ")
        cmd_list.append("java")  
        cmd_list.append("-jar")
        cmd_list.append(exe_name)
        cmd_string="["+"\"" + cmd_list[0] + "\""+","+"\"" + cmd_list[1] + "\""+","+"\"" + cmd_list[2] + "\""+"]"
        dockfile.write(cmd_string)
        dockfile.write("\n")
        #print("Dockerfile written successfully")
        return exe_path

def build_image(dockfilepath):
    os.chdir(dockfilepath)
    os.system(docker_commands['build_image'])
    

def launch_image(imagepath,logpath):
    print("Executiion in test....")
    t1=Thread(target=check_stats,args=(imagepath,logpath,))
    t1.start()
    os.system(docker_commands['launch_image'])
    cleanup()

def cleanup():
    os.remove("Dockerfile")