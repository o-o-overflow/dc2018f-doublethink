#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define str(x) #x
 
int main()
{
#ifndef SC_MAX_SIZE
  	int max_size = 0x2000;
#else
	int max_size = SC_MAX_SIZE;
#endif
#ifndef SC_ADDRESS
  	uintptr_t address = 0x10000;
#else
	#warning Hardoding address.
	uintptr_t address = SC_ADDRESS;
#endif

  	printf("Opening shellcode file...\n");
  	FILE *shellcode_file = fopen("shellcode", "r");
  	printf("... %p\n", shellcode_file);

#if defined SC_MAP_FILE
	puts("Mapping file...\n");
	#warning Memory-mapping shellcode.
  	void *mem = mmap((void *)address, 0x4000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE, fileno(shellcode_file), 0);
  	printf("Mapped shellcode at %p (tried for %p)...\n", mem, (void *)address);
#else
#ifdef SC_NO_MAP
	#warning Not mapping memory.
	void *mem = (void *)address;
#else
	puts("Mapping memory...\n");
  	void *mem = mmap((void *)address, 0x4000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
#endif
	printf("Reading file into %p...\n", mem);
  	int read_bytes = fread(mem, 1, max_size, shellcode_file);
  	printf("Loaded %d bytes of shellcode at %p (tried for %p)...\n", read_bytes, mem, (void *)address);
#endif

	printf("Executing!\n");

  	((void(*)())mem)();
}
