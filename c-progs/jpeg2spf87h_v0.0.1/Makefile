CC = gcc
CFLAGS = -Wall -O2 
STRIP = strip
# To retain the symbol tables for debugging, comment out the previous two lines,
# and uncomment the next two lines.
#CFLAGS = -Wall -g 
#STRIP = :
#LDFLAGS = -lusb-1.0 -lusb
LDFLAGS = -lusb-1.0 

OBJ=jpeg2spf87h

all: $(OBJ)
	$(STRIP) $(OBJ)

jpeg2spf87h: jpeg2spf87h.o
	${CC} ${CFLAGS} ${LDFLAGS} jpeg2spf87h.o -I/home/ullix/websites/local/photoframe/jpeg2spf87h_v0.0.1 -o jpeg2spf87h

jpeg2spf87h.o: jpeg2spf87h.c
	${CC} ${CFLAGS} ${LDFLAGS} -I/home/ullix/websites/local/photoframe/jpeg2spf87h_v0.0.1 -c jpeg2spf87h.c
	
clean:
	rm -rf *.o jpeg2spf87h
