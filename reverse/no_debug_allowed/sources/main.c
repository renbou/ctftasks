#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/ptrace.h>

extern char _start;
extern char __etext;

typedef uint64_t uint64;

uint64 flag[] = {14553168476468515318ULL,
3608753297938334990ULL,
14884977645541167323ULL,
2318412652970800634ULL,
6091453452162891230ULL,
13552539919290486868ULL,
6062369165789014876ULL,
1222854938220773060ULL};
uint64 rol(uint64 x, uint64 n) {
	__asm__ volatile (
		"mov %[x], %%rax\n"
  		"mov %[n], %%rcx\n"
		"rol %%cl, %%rax\n"
  		"mov %%rax, %[x]"
		: [x]"+r"(x)
		: [n]"r"(n)
		: "cc", "memory"
		);
	return x;
}

uint64 calcHash() {
	unsigned char *start = (unsigned char *)&_start;
	unsigned char *end = (unsigned char *)&__etext;
	uint64 hash = 0xbebebefefefebefe;
	while (start != end) {
		hash = rol(hash, 13) ^ (*(uint8_t *)start);
		if (((uint64)start % 2) == 0) {
			hash = ((hash & 0xFFFFFFFF00000000ULL) >> 32) | (hash << 32);
		} else {
			hash = ((hash & 0x0000FFFF00000000ULL) << 16) | ((hash & 0xFFFF000000000000ULL) >> 16) |
				   ((hash & 0x000000000000FFFFULL) << 16) | ((hash & 0x00000000FFFF0000ULL) >> 16);
		}
		start++;
	}
	return hash;
}

int main() {
	if (ptrace(PT_TRACE_ME, 0, 1, 0) == -1) {
		printf("No debug allowed\n");
		return 0;
	}
	uint64 hash = calcHash();
	//printf("Current Hash is: %llu\n", hash);
	printf("Enter the password:\n");
	for (int i = 0; i < 8; i++) {
		uint64 cur;
		scanf("%llu", &cur);
		if ((cur ^ hash) != flag[i])
			return 0;
		hash ^= rol(cur, 17);
	}
	printf("Yep, it's correct!\n");
	return 0;
}
