#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

void encodeHamming(int data[4], int encoded[7]) {
    encoded[2] = data[0];
    encoded[4] = data[1];
    encoded[5] = data[2];
    encoded[6] = data[3];

    encoded[0] = encoded[2] ^ encoded[4] ^ encoded[6];
    encoded[1] = encoded[2] ^ encoded[5] ^ encoded[6];
    encoded[3] = encoded[4] ^ encoded[5] ^ encoded[6];
}

void introduceError(int encoded[7]) {
    int pos = rand() % 7;
    printf("Introducing an error at bit position %d\n", pos + 1);
    encoded[pos] = 1 - encoded[pos];
}

void correctHamming(int received[7]) {
    int c1 = received[0] ^ received[2] ^ received[4] ^ received[6];
    int c2 = received[1] ^ received[2] ^ received[5] ^ received[6];
    int c3 = received[3] ^ received[4] ^ received[5] ^ received[6];

    int error_pos = c3 * 4 + c2 * 2 + c1;

    if (error_pos != 0) {
        printf("Error detected at bit position: %d\n", error_pos);
        received[error_pos - 1] = 1 - received[error_pos - 1];
    } else {
        printf("No error detected.\n");
    }
}

int main() {
    srand(time(NULL));

    int data[4] = { 1, 0, 1, 1 };
    int encoded[7];
    int corrupted[7];

    printf("Original message:  ");
    for (int i = 0; i < 4; i++) printf("%d", data[i]);
    printf("\n");

    encodeHamming(data, encoded);

    printf("Encoded message:   ");
    for (int i = 0; i < 7; i++) {
        printf("%d", encoded[i]);
        corrupted[i] = encoded[i];
    }
    printf("\n");

    introduceError(corrupted);

    printf("Corrupted message: ");
    for (int i = 0; i < 7; i++) printf("%d", corrupted[i]);
    printf("\n");

    correctHamming(corrupted);

    printf("Corrected message: ");
    for (int i = 0; i < 7; i++) printf("%d", corrupted[i]);
    printf("\n");

    return 0;
}
