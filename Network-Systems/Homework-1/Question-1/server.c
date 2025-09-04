#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char *message = "Hello, Client!";

    // Step 1: Create a socket
    // AF_INET for IPv4, SOCK_STREAM for TCP
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("Error creating socket");
        return 1;
    }

    // Step 2: Bind the socket to port 8080
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; 
    server_addr.sin_port = htons(8080);      

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error binding socket");
        close(server_fd);
        return 1;
    }

    // Step 3: Listen for incoming connections
    if (listen(server_fd, 5) < 0) {
        perror("Error listening for connections");
        close(server_fd);
        return 1;
    }

    printf("Server listening on port 8080...\n");

    // Step 4: Accept a connection
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) {
        perror("Error accepting connection");
        close(server_fd);
        return 1;
    }
    printf("Client connected.\n");

    // Step 5: Send message to the client
    write(client_fd, message, strlen(message));

    // Step 6: Close the connection
    close(client_fd);
    close(server_fd);

    printf("Connection closed.\n");

    return 0;
}
