import socket
import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <server-hostname> <server-port> <input-file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    input_file_path = sys.argv[3]

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        sys.exit(1)

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # TASK 1: Create a TCP/IP socket and connect it to the server.
    # Hint: socket.socket(socket.AF_INET, socket.SOCK_STREAM) creates the socket.
    # Then call sock.connect((hostname, port)) to connect.
    
    sock = socket.socket(socket.AF_INET, socket)
    try:
        # Attempt to connect to the server at the specified hostname and port
        sock.connect((hostname, port))
        # Catch all socket-related errors 
    except socket.error as e:
        print(f"Connection error:{e}")
        sys.exit(1)


    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 2)
            cmd = parts[0]
            message = ""

            # TASK 2: Build the protocol message string to send to the server.
            # Format:  "NNN X key"        for READ / GET
            #          "NNN P key value"   for PUT
            # where NNN is the total message length as a zero-padded 3-digit number,
            # X is "R" for READ and "G" for GET.
            # Hint: for READ/GET, size = 6 + len(key). For PUT, size = 7 + len(key) + len(value).
            # Reject lines with invalid format or key+" "+value > 970 chars.
            
            # Check if the current command is "READ"
            if cmd == "READ":
                # Calculate total length
                total_len = 6 + len(key)
                content = f"R {key}"
            # Check if the current command is "GET"
            elif cmd == "GET":
                # Calculate total length
                total_len = 6 + len(key)
                content = f"G {key}"
            # Check if the current command is "PUT"
            elif cmd =="PUT":
                # Calculate total length
                total_len = 7 + len(key) + len(value)
                content = f"P {key} {value}"
            # Length limit check
            key_value_str = f"{key} {value}"
            if len(key_value_str) > 970 or total_len > 999:
                print(f"{line}:ERR message too long")
                continue
            # Format the total length into a 3-digit string with leading zeros
            len_str = f"{total_len:03d}"
            message = len_str + content


            # TASK 3: Send the message to the server, then receive the response.
            # - Send:    sock.sendall(message.encode())
            # - Receive: first read 3 bytes to get the response size (like the server does).
            #            Then read the remaining (size - 3) bytes to get the response body.

            sock.sendall(message.encode())
            resp_len_bytes = sock.recv(3)
            # If no bytes are received, the server has closed the connection
            if not resp_len_bytes:
                print(f"{line}: ERR server closed connection")
                break
            # Decode the received 3-byte length header to string, then convert to integer to get the total response length
            resp_len = int(resp_len_bytes.decode())
            # Read the remaining content: total length - 3
            response_buffer = sock.recv(resp_len - 3)
            response = response_buffer.decode().strip()
            print(f"{line}: {response}")

    except (socket.error, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # TASK 4: Close the socket when done (already called for you — explain why
        # finally: is the right place to do this even if an error occurs above).
        sock.close()

if __name__ == "__main__":
    main()