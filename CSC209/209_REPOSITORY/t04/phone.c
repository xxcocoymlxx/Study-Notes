#include <stdio.h>
#include <stdlib.h>

int main() {

    int position;
    char phone[10];

    // Use scanf to read an integer followed by a string of length 10
    while (scanf("%s %d", phone, &position) != EOF) {
        if (position == 0) {
            printf("%s\n", phone);
        } else {
            printf("%c\n", phone[position]);
        }
    }
    return 0;
}
