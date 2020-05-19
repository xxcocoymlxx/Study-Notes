#include <stdio.h>
#include <stdlib.h>

#include "ptree.h"


int main(int argc, char *argv[]) {
    // Creates a ptree to test printing
    struct TreeNode root, child_one, child_two, grandchild;
    root.name = "root process";
    root.child_procs = &child_one;
    root.next_sibling = NULL;

    child_one.name = "first child";
    child_one.child_procs = NULL;
    child_one.next_sibling = &child_two;

    child_two.name = "second child";
    child_two.child_procs = &grandchild;
    child_two.next_sibling = NULL;

    grandchild.name = "grandchild";
    grandchild.child_procs = NULL;
    grandchild.next_sibling = NULL;

    print_ptree(&root, 0);

    return 0;
}

