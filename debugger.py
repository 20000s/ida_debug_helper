
# by 20000s 2022.5.3
from adbutils import adb
from sqlalchemy import true
import os
import threading
import time
import random
PACKAGE_NAME = ""
SO_NAME = ""
DIR_PATH = "/data/local/tmp/"


def jdb_connect():
    os.system("jdb -connect com.sun.jdi.SocketAttach:hostname=127.0.0.1,port=8700")


def start_debug(package_name,so_name):
    PACKAGE_NAME = package_name
    SO_NAME = so_name
    print("--------------start debugging------------------------")
    d = adb.device()
    adb.forward(d.serial,"tcp:23946","tcp:23946")
#    for item in adb.forward_list():
#        print(item.serial, item.local, item.remote)

    d.shell("am set-debug-app -w " + PACKAGE_NAME)
    print("plz click " + PACKAGE_NAME)
    while true:
        tmp = d.shell("ps -A | grep " + PACKAGE_NAME)
        if( PACKAGE_NAME in tmp):
            break
  
    print(PACKAGE_NAME + "has been open")
    line1 = d.shell("ps -A | grep " + PACKAGE_NAME)
    line1_list = line1.split()
    pid = int(line1_list[1])
    print(PACKAGE_NAME + " pid :" + str(pid))
    adb.forward(d.serial,"tcp:8700","jdwp:"+str(pid))
    print("plz use ida to attach "+ PACKAGE_NAME)
    ida_dbg.set_remote_debugger("127.0.0.1",None)
    attach_process(pid,1)
    print("debugger on")
    set_debugger_options(DOPT_LIB_BPT | DOPT_THREAD_BPT)
    t1 = threading.Thread(target = jdb_connect)
    t1.start()
    print("ok")
    # adbutil无root fuck
    # CMD = "cat /proc/" + str(pid) + "/maps | grep " + SO_NAME
    # BASE = ""
    # while true:
    #     tmp = d.shell(CMD)

    #     if(tmp):
    #         print(tmp)
    #         tmp = tmp.split()
    #         for i in range(len(tmp)):
    #             if tmp[i] == "r-xp":
    #                 BASE = tmp[i-1]
    #                 break
    #         BASE = BASE.split("-")[0]
    #         BASE = int(BASE,16)
    #         break

    #     else:
    #         ida_dbg.continue_process()
    # print(BASE)
    ida_dbg.continue_process()
    ida_dbg.wait_for_next_event(WFNE_SUSP,1)
    has_so = False
    while True:
        module_base = get_first_module()
        while module_base != None:
            module_name = get_module_name(module_base)
            if module_name.find(SO_NAME) >= 0:
                has_so = True
                break
        
            module_base = get_next_module(module_base)
        if has_so:
            break
        else : 
            ida_dbg.continue_process()
            ida_dbg.wait_for_next_event(WFNE_SUSP,1)  
    module_size = get_module_size(module_base)
    print('[*]found so base=>0x%08X, Size=0x%08X' % (module_base, module_size))

def dump(ea_start,ea_end):
    print('[*]begin to dump segment')
    save_file = DIR_PATH + PACKAGE_NAME + str(random.randint(0,10000))
    handle_f = open(save_file, 'wb')
    for byte_addr in range(ea_start, ea_end):
        byte_value = idaapi.get_byte(byte_addr)
        handle_f.write(struct.pack('B',byte_value))
    
    handle_f.close()
    hooks = idaapi.DBG_Hooks()
    hooks.hook()
    print("[*] saved in " + save_file)




    

