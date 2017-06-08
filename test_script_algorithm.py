from jared_algorithm import TableData



if(TableData(20,6,23,90,60,0,0,0,0,0,0,0,0,0,0,0,97330,0)=='very good'):
    print "TEST VERY GOOD PASSED"
else:
    print "TEST VERY GOOD FAILED!"
    
if(TableData(30,5,25,110,70,0,0,0,0,0,0,0,0,0,0,0,97231,0)=='good'):
    print "TEST GOOD PASSED"
else:
    print "TEST GOOD FAILED!"

if(TableData(40,3,26,120,80,1,1,1,1,1,1,1,1,1,1,1,97456,1)=='average'):
    print "TEST AVERAGE PASSED"
else:
    print "TEST AVERAGE FAILED"

if(TableData(50,2,28,130,100,1,1,1,1,1,1,1,1,1,1,1,97312,1)=='bad'):
    print "TEST BAD PASSED"
else:
    print "TEST BAD FAILED"
if(TableData(60,1,30,140,120,1,1,1,1,1,1,1,1,1,1,1,97265,1)=='very bad'):
    print "TEST VERY BAD PASSED"
else:
    print "TEST VERY BAD FAILED"
    
   
