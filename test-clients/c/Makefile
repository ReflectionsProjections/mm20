CC=/usr/bin/gcc
CC_OPTS=-g3
CC_LIBS=
CC_DEFINES=
CC_INCLUDES=
CC_ARGS=${CC_OPTS} ${CC_LIBS} ${CC_DEFINES} ${CC_INCLUDES}

# clean is not a file
.PHONY=clean

all: client

client: clientConnect.c clientAI.c AIObjects.c
	@${CC} ${CC_ARGS} -o client clientConnect.c

clean:
	@rm -f client *.o