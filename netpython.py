import argparse
import socket
import threading


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", action="store_true", help="Used to specify that netpython should listen "
                                             "for an incoming connection rather than "
                                             "initiate a connection to a remote host.")
    parser.add_argument("-t", type=str, default="localhost", help="Ip address to create server or to connect to")
    parser.add_argument("-p", type=int, help="Specifies the source port netpython should "
                                             "use, subject to privilege restrictions "
                                             "and availability.")

    args = parser.parse_args()

    if args.l:
        listen(args.t, args.p)


def listen(ip, port):
    try:
        ipv = socket.AF_INET6 if ":" or ip == "localhost" in ip else socket.AF_INET

        server = socket.socket(ipv, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(1)
        print(f"listing on {ip}:{port}...")

        while True:
            client, addr = server.accept()
            print(f"Connection to {addr}!")
            client.send(b"hi there you connected\n")
            recv_thread = threading.Thread(target=handle_client_recv,
                                           args=(client,))
            send_thread = threading.Thread(target=handle_client_send,
                                           args=(client,))

            recv_thread.start()
            send_thread.start()

            recv_thread.join()
            send_thread.join()
    except KeyboardInterrupt:
        print()  # this print is just here because other wise a % show up when you interupt and I didn't like it
    except Exception as e:
        print(f"An error has occurred: {e}")
    finally:
        server.close()


def handle_client_recv(client):
    try:
        while True:
            data = client.recv(1024)  # Receive data from the client
            print(data.decode(), end="")
    except Exception as e:
        print(f"An error has occurred: {e}")


def handle_client_send(client):
    try:
        while True:
            message = input()
            client.send((message + "\n").encode())
    except Exception as e:
        print(f"An error has occurred: {e}")


if __name__ == "__main__":
    main()
