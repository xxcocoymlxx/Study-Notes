#include <stdio.h>
#include <stdlib.h>
#include "bitmap.h"


int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: bitmap_printer input_bmp\n");
        exit(1);
    }

    FILE *image = fopen(argv[1], "rb");
    if (image == NULL) {
        fprintf(stderr, "Cannot open file\n");
        exit(1);
    }

    // Read in bitmap file metadata
    int pixel_array_offset, width, height;
    read_bitmap_metadata(image, &pixel_array_offset, &width, &height);

    // Print out metadata.
    printf("Pixel array offset: %d\n", pixel_array_offset);
    printf("Width: %d\n", width);
    printf("Height: %d\n", height);

    // Remove the next line once you start writing read_pixel_array
    //return 0;

    // Read in the pixel data
    struct pixel **pixels = read_pixel_array(image, pixel_array_offset, width, height);

    // Print out some pixels from each of the image's corners.
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            print_pixel(pixels[i][j]);
            print_pixel(pixels[i][width - 1 - j]);
            print_pixel(pixels[height - 1 - i][j]);
            print_pixel(pixels[height - 1 - i][width - 1 - j]);
        }
    }

    //free the space allocated for the 2D array
    for (int i = 0; i < height; i++){
         free(pixels[i]);
    }
    free(pixels);
    fclose(image);//上面fopen过的东西一定要记得关，不然总会有一个memory leak
    
//现在我run valgrind的结果就是:
/*
==18307== HEAP SUMMARY:
==18307==     in use at exit: 0 bytes in 0 blocks
==18307==   total heap usage: 204 allocs, 204 frees, 131,368 bytes allocated
==18307== 
==18307== All heap blocks were freed -- no leaks are possible
==18307== 
==18307== For counts of detected and suppressed errors, rerun with: -v
==18307== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
*/
    return 0;
}
