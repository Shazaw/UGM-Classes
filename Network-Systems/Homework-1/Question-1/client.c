#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int client_fd;
    struct sockaddr_in server_addr;
    char buffer[1024] = {0};

    // Step 1: Create a socket
    client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd < 0) {
        perror("Error creating socket");
        return 1;
    }

    // Step 2: Define server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080); // Port 8080

    // Convert IPv4 address from text to binary form
    if(inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        close(client_fd);
        return 1;
    }

    // Step 3: Connect to the server
    if (connect(client_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error connecting to server");
        close(client_fd);
        return 1;
    }
    printf("Connected to server.\n");

    // Step 4: Receive message from the server
    read(client_fd, buffer, sizeof(buffer) - 1); // Read data into buffer
    printf("Received from server: %s\n", buffer);

    // Step 5: Close the connection
    close(client_fd);

    return 0;
}
