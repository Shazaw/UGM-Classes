#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 9090

int main() {
    int client_fd;
    struct sockaddr_in server_addr;
    char *message = "Hello from TCP Client!";
    char buffer[1024] = {0};

    // Create a TCP socket
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation failed");
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    // Convert address to binary
    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        return 1;
    }

    // Connect to the server
    if (connect(client_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        return 1;
    }

    // Send message to the server
    write(client_fd, message, strlen(message));
    printf("Message sent to server.\n");

    // Receive echoed message from server
    read(client_fd, buffer, 1024);
    printf("Received from server: %s\n", buffer);

    // Close the socket
    close(client_fd);

    return 0;
}
