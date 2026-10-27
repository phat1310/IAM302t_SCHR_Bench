#include <stdio.h>
#include <stdlib.h>
extern int target(int,int,int);
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "expected exactly three integer arguments\n"); return 2; }
    int a=(int)strtol(argv[1],NULL,0);
    int b=(int)strtol(argv[2],NULL,0);
    int c=(int)strtol(argv[3],NULL,0);
    printf("%d\n",target(a,b,c));
    return 0;
}
