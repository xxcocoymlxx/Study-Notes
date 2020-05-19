#include <stdio.h>
//1
struct file{
    int size;
    char permission[15];
    char file_name;
} f1,f2,f3;//这样就直接define了f1,f2和f3

//2
//如果这个type的东西你只用一次，你甚至可以都不给他名字
struct {
    int size;
    char permission[15];
    char file_name;
} f1,f2,f3;//这时就只能这个declare这个type的object了

//3
typedef struct file{
    int size;
    char permission[15];
    char file_name;
}
//现在如果你要declare一个这个type的variable就直接
//file f1;就可以了

//linked struct
//struct之后也可以包含其他类型的struct
//现在就可以不是fixed size了
struct file{
    int size;
    char permission[15];
    char file_name;
    file *next = NULL;
}
//此时创建他的object的时候一般就按照这个struct的pointer来建，不按照这个struct本身来建
//如果是这个struct的pointer要access这个struct的member，用->
