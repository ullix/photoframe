CC = gcc
CFLAGS = -Wall -O2
STRIP = strip
# To retain the symbol tables for debugging, comment out the previous two lines,
# and uncomment the next two lines.
#CFLAGS = -Wall -g 
#STRIP = :

LDFLAGS = -lusb-1.0 

OBJ=spf87hd

all: $(OBJ)
	$(STRIP) $(OBJ)

spf87hd: spf87hd.o
	${CC} ${CFLAGS} ${LDFLAGS} spf87hd.o -o spf87hd

spf87hd.o: spf87hd.c
	${CC} ${CFLAGS} ${LDFLAGS} -c spf87hd.c

clean:
	rm -rf *.o spf87hd


