CC = gcc
CFLAGS = -Wall -O2
LDFLAGS = -lrt -lusb -ljpeg

OBJ=playusb

all: $(OBJ)

playusb: playusb.o fbgrab.o
	${CC} ${CFLAGS} ${LDFLAGS} -I/usr/src/linux-headers-3.0.0-13/include/ playusb.o fbgrab.o -o playusb


playusb.o: playusb.c
	${CC} ${CFLAGS} ${LDFLAGS} -I/usr/src/linux-headers-3.0.0-13/include/ -c playusb.c
	
fbgrab.o: fbgrab.c
	${CC} ${CFLAGS} ${LDFLAGS} -I/usr/src/linux-headers-3.0.0-13/include/ -c fbgrab.c
	
clean:
	rm -rf *o playusb
