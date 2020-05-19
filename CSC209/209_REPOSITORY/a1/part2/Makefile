SHELL = /bin/bash
FLAGS = -Wall -Werror -std=c99
.PHONY: all test_vs clean

all: test_vs

validate_sin: validate_sin.o sin_helpers.o
	gcc ${FLAGS} -o $@ $^

%.o: %.c
	gcc ${FLAGS} -c $<

test_vs: validate_sin
	@test_vs_output=`./validate_sin 810620716`; \
	if [ "$$test_vs_output" == "Valid SIN" ]; then \
		echo Compiled and sanity check passed; \
	else \
		echo Failed sanity check; \
	fi

clean:
	rm -f *.o validate_sin
