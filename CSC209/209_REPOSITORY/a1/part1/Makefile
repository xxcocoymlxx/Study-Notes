SHELL = /bin/bash
FLAGS = -Wall -Werror -std=c99
.PHONY: all test_cl clean

all: test_cl

count_large: count_large.o 
	gcc ${FLAGS} -o $@ $^

%.o: %.c 
	gcc ${FLAGS} -c $<

test_cl: count_large
	@test_cl_output=`./count_large 1000 rwx------ < test_inputs/handout.test`; \
	if [ ! -z "$$test_cl_output" ] && [ "$$test_cl_output" -eq 2 ]; then \
		echo Compiled and sanity check passed; \
	else \
		echo Failed sanity check; \
	fi 

clean: 
	rm -f *.o count_large
