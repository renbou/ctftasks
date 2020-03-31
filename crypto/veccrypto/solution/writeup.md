# Veccrypto
## Writeup
After having defined a vector and vector multiplication the needed way, it seems difficult for us to get the vector A from A*B=C by dividing, since C/A=B but C/B does not equal to A. However, C.conj() (the normal vector part of C negated) divided by B gives us A, using which we can later simply decode the rest of the ciphertext.