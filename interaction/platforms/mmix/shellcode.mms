* what the crap omg

         LOC  #200
Main     GETA  $255,4F
         TRAP 0,Fopen,3
         GETA $255,5F
         TRAP 0,Fread,3
         GETA $255,5F
         TRAP 0,Fwrite,StdOut
         TRAP 0,Halt,0
4H       OCTA 3F,TextRead
         LOC  (@+3)&-4
3H       BYTE "flag",0
         LOC  (@+3)&-4
5H       OCTA 6F,100
         LOC  (@+3)&-4
6H       OCTA @+100
