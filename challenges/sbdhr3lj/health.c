#include <stdio.h>
#include <unistd.h>

int main(void) {
    seteuid(0);
    setegid(0);
    setuid(0);
    setgid(0);


    // check the output of the command ps -aux | grep kafka
    // if the kafka process is running, return 0
    // else return 1
    if (system("ps -a | grep kafka | grep -v grep") == 0) {
        printf("Kafka is running\n");
        return 0;
    } else {
        printf("Kafka is not running\n");
        return 1;
    }

    return 0;
}
    