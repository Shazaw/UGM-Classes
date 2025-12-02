import socket
import datetime

HOST = "127.0.0.1"   # Localhost
PORT = 50007        # Make sure client uses the same port


def timestamp() -> str:
    """Return current time as [HH:MM:SS]."""
    return datetime.datetime.now().strftime("[%H:%M:%S]")


def main() -> None:
    server_name = input("Enter server name: ").strip() or "Server"

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow quick reuse of port if you restart the program
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind and listen
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"{timestamp()} {server_name} listening on {HOST}:{PORT} ...")

        # Wait for one client to connect
        conn, addr = server_socket.accept()
        print(f"{timestamp()} Connected by {addr}")

        with conn:
            while True:
                # Receive message from client
                data = conn.recv(1024)
                if not data:
                    print(f"{timestamp()} Client disconnected.")
                    break

                msg = data.decode().strip()
                print(f"{timestamp()} Client: {msg}")

                # If client sends /quit, end chat
                if msg.lower() == "/quit":
                    print(f"{timestamp()} Client requested to end the chat.")
                    break

                # Ask server user for reply
                reply = input(f"{timestamp()} {server_name}: ")
                conn.sendall(reply.encode())

                # Server can also end chat with /quit
                if reply.strip().lower() == "/quit":
                    print(f"{timestamp()} Chat ended by server.")
                    break


if __name__ == "__main__":
    main()
