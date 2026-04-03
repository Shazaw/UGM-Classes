import socket
import datetime

HOST = "127.0.0.1"   # Server IP (localhost for this assignment)
PORT = 50007        # Must match server's port


def timestamp() -> str:
    """Return current time as [HH:MM:SS]."""
    return datetime.datetime.now().strftime("[%H:%M:%S]")


def main() -> None:
    client_name = input("Enter your chat name: ").strip() or "Client"

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"{timestamp()} Connected to server at {HOST}:{PORT}")

        while True:
            # Get message from user
            message = input(f"{timestamp()} {client_name}: ")

            # Send to server
            client_socket.sendall(message.encode())

            # If client wants to quit, stop after sending
            if message.strip().lower() == "/quit":
                print(f"{timestamp()} You ended the chat.")
                break

            # Wait for server reply
            data = client_socket.recv(1024)
            if not data:
                print(f"{timestamp()} Server closed the connection.")
                break

            reply = data.decode().strip()
            print(f"{timestamp()} Server: {reply}")

            # If server sends /quit, end chat
            if reply.lower() == "/quit":
                print(f"{timestamp()} Server ended the chat.")
                break


if __name__ == "__main__":
    main()
