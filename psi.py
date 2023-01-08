import serial
from serial.tools import list_ports
from time import sleep,strftime

ver = "1.0"
cmd = ""
prt = ""
quitStatements = ["q","quit","exit","leave","bye"]
helpdict = {"list":"lists all available serial ports","connect <port>":"connects to the port specified. typing the port by itself will do the same as this command."}
chelpdict = {"disconnect":"disconnects psi from your playdate","script <script>":"executes a psi script"}

def writelog(log,cmd,data=""):
    log.write("<"+strftime("%H:%M:%S")+"> ("+cmd+") "+data)

def execute(cmd,ser,log):
    try:
        ser.write(cmd.encode()+b"\r\n")
    except serial.SerialException:
        ser.close()
        ser = serial.Serial(port=prt, baudrate=115200, bytesize=8, parity='N')
        ser.write(cmd.encode()+b"\r\n")
    sleep(0.1)

    if cmd == "datadisk" or cmd == "bootdisk":
        writelog(log,cmd,"")
        input("press enter when you've ejected your playdate...")
        ser.close()
        ser = serial.Serial(port=prt, baudrate=115200, bytesize=8, parity='N')
    else:
        data = "".join(ser.read_all().decode().split(cmd+"\r\n")[1:])

        writelog(log,cmd,data.replace("\r\n","\n")+"\n")
        print(data)

print("\npsi version "+ver+". type 'help' for help.\n")

while True:
    cmd = input("psi> ")
    if cmd.startswith("connect ") or cmd.startswith("COM") or cmd.startswith("/dev/"):
        if prt.startswith("connect "):
            prt = cmd.split("connect ")[1]
        else:
            prt = cmd

        try:
            ser = serial.Serial(port=prt, baudrate=115200, bytesize=8, parity='N')

            log = open("psi.log","a+")
            print("connection established!")

            while True:
                cmd = input("psi/playdate@"+prt+"> ")
                if cmd in quitStatements or cmd == "disconnect":
                    log.close()
                    break
                elif cmd.startswith("script "):
                    cmd = cmd.split("script ")[1]
                    f = open(cmd,"r")
                    data = f.read().split("\n")
                    writelog(log,"script "+cmd,"\n")
                    for i in data:
                        if not i.startswith("~~") or len(i) == 0:
                            if i.startswith("wait "):
                                i = i.split("wait ")[1]
                                print("waiting for "+str(i)+" seconds...")
                                sleep(float(i))
                            elif i.startswith("*"):
                                i = "".join(i.split("*")[1:])
                                times = int(i.split(" ")[0])
                                command = " ".join(i.split(" ")[1:])
                                print("running '"+command+"' "+str(times)+" times...")
                                for z in range(times):
                                    execute(command,ser,log)
                                    sleep(0.125)
                            else:
                                print(i)
                                execute(i,ser,log)
                                sleep(0.125)
                    print("-- script finished! --\n")
                elif cmd.isspace() or cmd == "":
                    pass
                else:
                    execute(cmd,ser,log)
            ser.close()
            print("connection closed.")
        except serial.SerialException as s:
            print("err: could not open port "+prt+". is your playdate plugged in and unlocked? are you sure this is the right port?")

    elif cmd == "help":
        print("\n---- psi help ----\n\n-- while disconnected --\n")
        for c in helpdict:
            print(c+" - "+helpdict[c])
        print("\n-- while connected --\n")
        for c in chelpdict:
            print(c+" - "+chelpdict[c])

        print("\nworks everywhere: quit, help\n")

    elif cmd == "list":
        comports = list_ports.comports()
        if len(comports) != 0:
            print("available ports: ",end="")
            for i in comports:
                print(i.device,end=" ")
            print()
        else:
            print("err: there are no available ports! did you plug your playdate in?")
        
    elif cmd in quitStatements:
        quit()
    else:
        pass