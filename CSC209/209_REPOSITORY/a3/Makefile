FLAGS = -Wall -Werror -std=gnu99
LIBS = -lm
DEPENDENCIES = eratosthenes.h

all: pfact

pfact: pfact.o filter.o pipeline_stage.o
	gcc ${FLAGS} -o $@ $^ ${LIBS}

%.o: %.c ${DEPENDENCIES}
	gcc ${FLAGS} -c $< 

clean: 
	rm -f *.o pfact
