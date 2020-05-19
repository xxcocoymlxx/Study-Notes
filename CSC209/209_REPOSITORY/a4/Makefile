PORT = 55555
FLAGS = -DPORT=${PORT} -Wall -Werror -fsanitize=address -fsanitize=undefined -std=gnu99
DEPENDENCIES = socket.h jobprotocol.h

EXECS = jobserver
SUBDIRS = jobs

.PHONY: ${SUBDIRS} clean

all: ${EXECS} ${SUBDIRS}

${EXECS}: %: %.o jobprotocol.o socket.o
	gcc ${FLAGS} -o $@ $^

${SUBDIRS}:
	make -C $@

%.o: %.c ${DEPENDENCIES}
	gcc ${FLAGS} -c $<

clean:
	rm -f *.o ${EXECS}
	@for subd in ${SUBDIRS}; do \
        echo Cleaning $${subd} ...; \
        make -C $${subd} clean; \
    done
