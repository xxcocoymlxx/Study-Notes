FLAGS = -Wall -Werror -std=c99
.PHONY: all clean

all: invest score_card phone

invest: invest.o
	gcc ${FLAGS} -o $@ $^

score_card: score_card.o
	gcc ${FLAGS} -o $@ $^

phone: phone.o
	gcc ${FLAGS} -o $@ $^

%.o: %.c
	gcc ${FLAGS} -c $<

clean:
	rm -f *.o invest scorecard phone
