CC=/usr/bin/gcc
CC_OPTS=-g3
CC_LIBS=
CC_DEFINES=
CC_INCLUDES=
CC_ARGS=${CC_OPTS} ${CC_LIBS} ${CC_DEFINES} ${CC_INCLUDES}
LINK_ARGS=-ljansson

# clean is not a file
.PHONY=clean

all: client

client: main.c client_ai.c ai_objects.c utils.c parse_json.c
	@${CC} ${CC_ARGS} -o client main.c ${LINK_ARGS}

clean:
	@rm -f client *.o