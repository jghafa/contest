#include <stdio.h>
FILE *fp; 		// create a file pointer

int main()
{
char line[80];
fp = fopen("Input-01.txt", "rt");	// open up the file

while(fgets(line, 80, fp) != NULL)

{
printf(line);	// print the results to stdout
}
fclose(fp);
}