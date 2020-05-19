#FLAGS = -Wall -Werror -std=gnu99 
FLAGS = -Wall -Werror -g -std=gnu99 -DTEST
DEPENDENCIES = ptree.h

all: test_print print_ptree

test_print: test_print.o ptree.o
	gcc ${FLAGS} -o $@ $^

print_ptree: print_ptree.o ptree.o
	gcc ${FLAGS} -o $@ $^

%.o: %.c ${DEPENDENCIES}
	gcc ${FLAGS} -c $<

clean: 
	rm -f *.o test_print print_ptree
