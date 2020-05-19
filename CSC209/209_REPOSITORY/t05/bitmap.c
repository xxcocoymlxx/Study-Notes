#include <stdio.h>
#include <stdlib.h>
#include "bitmap.h"


/*
 * Read in the location of the pixel array, the image width, and the image 
 * height in the given bitmap file.
 */
void read_bitmap_metadata(FILE *image, int *pixel_array_offset, int *width, int *height) {
//Use fseek to navigate to different byte locations so that you only read the three 
//required integers. Then, you can use fread to read the expected number of bytes 
//into a variable of the type you want.
	
/*
size_t fread(void *ptr, size_t size, size_t n, FILE *fp);

The ptr is the starting address of the memory block where
data will be stored after reading from the file. The function
reads n items from the file where each item occupies the number 
of bytes specified in the second argument. On success, it reads n
 items from the file and returns n. On error or end of the file, 
 it returns a number less than n.
*/

	//At byte offset 10-13, where the pixel array starts.
	fseek(image,10,SEEK_SET);//fseek不读取文件信息，他只是移动position到我们要的东西那里
	fread(pixel_array_offset, sizeof(int), 1, image);


	// Image Width in pixels, At byte offset 18-21
	fseek(image,18,SEEK_SET);//from beginning of the file, jump to position 18 
	fread(width, sizeof(int), 1, image);
 	
 	// Image Height in pixels, At byte offset 22-25
	fseek(image,22,SEEK_SET);
	fread(height, sizeof(int), 1, image);

	//printf("%lu\n",sizeof(struct pixel));
	//it prints out 3.
}


/*
 * Read in pixel array by following these instructions:
 *
 * 1. First, allocate space for m "struct pixel *" values, where m is the 
 *    height of the image.  Each pointer will eventually point to one row of 
 *    pixel data.
 * 2. For each pointer you just allocated, initialize it to point to 
 *    heap-allocated space for an entire row of pixel data. (not pointer of pixel data)
 *						[so it's like a matrix]
 * 3. Use the given file and pixel_array_offset to initialize the actual 
 *    struct pixel values. 
 * 4. Return the address of the first "struct pixel *" you initialized.
 */
//我们先是建了一个竖着的array of pixel pointers，相当于每行array的（第一个element的）address
//我们现在要用loop把每一行的pointer都后面连上pixel（而不是pixel pointers）
//现在相当于是好多个array of pixel了叠在一起，而这matrix的第一列就是每行array的address（pointer）
//然后我们现在要从image这个file里用height和width读取出信息然后populate the matrix accordingly 

//So我们是把这个image里面的每个pixel按照他们的位置放到相对应的我们创建的这个matrix里
struct pixel **read_pixel_array(FILE *image, int pixel_array_offset, int width, int height) {
	//allocate space for the 2D array
	int i,j;
	struct pixel **pixel_data = malloc(sizeof(struct pixel *)*height);
	for (i = 0; i < height; i++){
		pixel_data[i] = malloc(sizeof(struct pixel)*width);
	}

	//from beginning of the file, jump to where the pixel array starts.
	//this works for every time you call fread().
	fseek(image,pixel_array_offset,SEEK_SET);

	//populate the matrix with pixels from the image into the 2D array
	for (i = 0; i < height; i++){
		for (j = 0; j < width; j++){
			fread(&pixel_data[i][j], sizeof(struct pixel), 1, image);
			//当你想复制给一个variable时记得要提供那个variable的地址，而不是pixel_data[i][j]本身
		}
	}
	return pixel_data;
}


/*
 * Print the blue, green, and red colour values of a pixel.
 * You don't need to change this function.
 */
void print_pixel(struct pixel p) {
    printf("(%u, %u, %u)\n", p.blue, p.green, p.red);
}
