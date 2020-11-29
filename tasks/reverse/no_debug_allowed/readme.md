# no_debug_allowed
## Description
how are you gonna solve reverse challenges without a debugger, huh?
## About + Writeup (solve.c in solution folder)
anti-debug executable, first checks for execution using ptrace, more as to fool the user into thinking that's the only thing they need to overcome. What you also need to do, however, is compute the hash without launching the debugger, because using a debugger will add 0xcc opcodes into the program, pretty much stopping it from computing the hash properly. Then just use the hash to xor back the flag vals.