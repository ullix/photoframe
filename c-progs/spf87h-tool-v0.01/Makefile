CC = gcc
CFLAGS = -Wall -O2
LDFLAGS = -lusb-1.0

OBJ=spf87h-tool

all: $(OBJ)

spf87h-tool: spf87h-tool.o
	${CC} ${CFLAGS} ${LDFLAGS} -I/usr/src/linux-headers-3.0.0-13/include/ -v spf87h-tool.o -o spf87h-tool

spf87h-tool.o: spf87h-tool.c
	${CC} ${CFLAGS} ${LDFLAGS} -I/usr/src/linux-headers-3.0.0-13/include/ -v -c spf87h-tool.c
	
clean:
	rm -rf *.o spf87h-tool
