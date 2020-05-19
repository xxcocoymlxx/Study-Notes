#include <stdio.h>
#include <stdlib.h>


struct ll_node {
    int value;
    struct ll_node *next;
};


// This overly complex code reads integers from stdin and places them in 
// a linked list. Then, it sums the items in the list and prints the result.
int main() {
    int user_inp;
    int sum;

    // Using a dummy head node
   //This is where the uninitialized variable comes from
   //The "front" has not been assignt to any value
    struct ll_node *front = malloc(sizeof(struct ll_node));
	   front->value = 0;
    struct ll_node *current = front;
    
    struct ll_node *head = front;//这里我们在一开始就让head指向了front
	//所以之后就算front和current都指向了linked list的最后一位，我们还是拥有了第一位的reference

   //在这个loop结束以后，current指向了linked list的最后一位
    while (scanf("%d", &user_inp) != EOF) {
        current->next = malloc(sizeof(struct ll_node));
        current = current->next;

        current->value = user_inp;
        current->next = NULL;
    }

    //在这个loop结束以后，front指向了linked list的最后一位
    for (sum = 0; front != NULL; front = front->next) {
        sum += front->value;
    }
    printf("The sum of the inputs is %d.\n", sum);
//after print the sum (don't need the linked list anymore) just free them
//here 我们就从head开始free，就可以free完了
 struct ll_node *temp;
    while(head!=NULL){
	temp = head;
	head = head->next;
	free(temp);
    }

    return 0;
}

