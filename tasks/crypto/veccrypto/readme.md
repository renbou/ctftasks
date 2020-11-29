# Veccrypto
## Description
i made this cool ass new cryptosystem using vector division and its 1000% uncrackable, you can use it to encrypt your own stuff mate (i wrote some comments in the server so you can understand how to implement it)
## About
If we define a vector as a pair of a scalar number and a normal 3d vector e.g \[a, \[b, c, d\]\] then we can add such vectors, multiply them, and even divide.  
Addition of example vectors \[0, \[1, 2, 3\]\] and \[-1, \[3, 1, 2\]\] would be done as normal vector addition, e.g = \[0+(-1), \[1+3, 2+1, 3+2\]\].  
Subtraction is same, except we negate all the elements in the vector \(\[-a, \[-b, -c, -d\]\]\).
\(\[a, A\] representation is the short form meaning small a is the scalar and A is the normal vector\)  
Now let's difine the multiplication of two such vectors as \[a, A\] * \[b, B\] = \[a\*b + (A,B), a\*B - b\*A + \[A, B\]\]
where \(A, B\) is the scalar multiplication of two normal vectors A and B and \[A, B\] is their cross product.

Now division works like this:
if A\*B = C, then B = C/A and A = C.conj\(\)/B  
conj\(\) is the same vector with the scalar part non-negated and the vector part negated
inverse\(\) is the vector divided by the sum of squares of all of its parts \(a\*a + b\*b + c\*c + d\*d\)

And division of C by A would be done as C \* A.inverse\(\).conj\(\)

\(it is correct because A\*A^-1 = A\*A.inverse\(\) = \[1, \[0, 0, 0\]\]\)
