FLAGS = -Wall -Werror -std=gnu99

all: randprint fastjob fastjob_stderr slowjob longprint
.PHONY: clean

longprint: longprint.o
	@gcc ${FLAGS} -o $@ $^ 

fastjob: fastjob.o
	@gcc ${FLAGS} -o $@ $^ 

fastjob_stderr: fastjob_stderr.o
	@gcc ${FLAGS} -o $@ $^ 

slowjob: slowjob.o
	@gcc ${FLAGS} -o $@ $^ 

randprint: randprint.o 
	@gcc ${FLAGS} -o $@ $^ 

%.o: %.c 
	@gcc ${FLAGS} -c $<

clean:
	rm -f *.o randprint fastjob fastjob_stderr slowjob longprint
