#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef Link_list{
	int i;
	Link_list next* = NULL;
}



int add(int i , Link_list **l){

	if (*l == NULL)
	{
		Link_list *head = malloc(sizeof(Link_list));
		head->i = i
		*l = head;

		return 0;
	}

	else
	{
		Link_list *head = *l;
		Link_list *curr;
		Link_list *node = malloc(sizeof(Link_list));
		node->i = i;

		curr = head;
		while(curr!= NULL&&curr->next!=NULL){
			if (curr->i < i && (curr->next)->i >= i)
			{
				node->next = curr->next;
				curr->next = node;
				return 0;
			}
			else
			{
				curr = curr->next;
			}
		}

		if(i < head->i){
			node->next = head;
			*l = node;
		}
		else{
			curr->next = node;
		}
		return 0;

	}

}


int remove(int i, Link_list **l){
	Link_list *head = &l;
	Link_list *curr;


	if (head->i == i)
	{
		Link_list *node;
		node = head->next;
		head->next = NULL;

		//l = &node; é”™è¯¯ï¼Œ lå‘ç”Ÿäº†å˜åŒ–
		*l= node;

		return 0;
	}


	curr = head;
	while(curr->next!= NULL){
		if ((curr->next)->i == i)
		{
			Link_list *node;
			node = curr->next;
			curr->next = node->next;
			node->next = NULL;
			return 0;
		}
		else{
			curr = curr->next;
		}
	}
	return 1;
}


int find(int i , Link_list *l){
	Link_list *curr =  l;

	while(curr != NULL){
		if (curr->i == i)
		{
			return 0;
		}
		curr = curr->next;
	}
	return 1;
}





int main(int argc, char const *argv[])
{
	Link_list *l;
	add(1,&l);
	add(2,&l);
	add(3,&l);


	remove(3,&l);
	remove(1,&l);

	Link_list *curr;
	Link_list *next;
	while(curr!= NULL){
		curr->next = next;
		free(curr);
		curr = next;
	}

	return 0;
}