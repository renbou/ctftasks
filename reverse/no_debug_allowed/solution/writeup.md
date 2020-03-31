#no_debug_allowed
##Writeup
First let's decompile with ghidra or ida, this file isn't stripped or optimized, it decompiles well, then let's use something like r2 to get the buffers needed after which we simply get the hash and then reverse the flag with xor and rol.