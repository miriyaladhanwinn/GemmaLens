/*
Sample Vulnerable C Program for GemmaLens Demonstration
Demonstrating:
1. Heap memory leak (missing free)
2. Out-of-bounds array write (buffer overflow)
3. Dangling pointer dereference after stack frame exit
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Vulnerability 1: Returning pointer to local stack variable (Dangling Pointer)
char *get_local_buffer() {
    char stack_buf[32];
    strncpy(stack_buf, "Temporary Stack Data", sizeof(stack_buf));
    return stack_buf; // Bug: stack_buf destroyed when function returns
}

// Vulnerability 2: Off-by-one buffer overflow in loop condition
void write_buffer(int *dest, int count) {
    for (int i = 0; i <= count; i++) { // Bug: '<=' writes to count + 1 indices
        dest[i] = i * 10;
    }
}

int main() {
    printf("Starting vulnerable execution test...\n");

    // Vulnerability 3: Memory allocated on heap but never freed (Memory Leak)
    int *dynamic_array = (int *)malloc(5 * sizeof(int));
    if (!dynamic_array) {
        return 1;
    }

    write_buffer(dynamic_array, 5);

    printf("Buffer item 0: %d\n", dynamic_array[0]);

    char *leaked_msg = get_local_buffer();
    printf("Msg: %s\n", leaked_msg);

    // Missing: free(dynamic_array);
    return 0;
}
