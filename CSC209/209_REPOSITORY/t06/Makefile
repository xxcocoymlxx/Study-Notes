FLAGS = -Wall -Werror -std=gnu99
DEPENDENCIES = helpers.h
.PHONY: all basic_test clean

all: basic_test
#all: serialize deserialize

serialize: serialize.o helpers.o
	gcc ${FLAGS} -o $@ $^

deserialize: deserialize.o helpers.o
	gcc ${FLAGS} -o $@ $^

%.o: %.c ${DEPENDENCIES}
	gcc ${FLAGS} -c $<

basic_test: serialize deserialize
	@test_output=`./serialize < test.dat | ./deserialize`; \
	if [ "$$?" -eq 0 ]; then \
		echo Basic test passed; \
	else \
		echo Basic test failed; \
	fi 

clean: 
	rm -f *.o serialize deserialize