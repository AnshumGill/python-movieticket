lst=[1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0]
row=['A','B','C','D','E','F','G','I','J','K','L','M','N','O']
row_count=count=0
print("**Screen This Way**\n")
print("  1    2     3     4     5\n")
for i in lst:
        if(i==1):
                print("|\u039E|",end=' ')
                count+=1
        elif(i==0):
                print("|_|",end=' ')
                count+=1
        if(count%5==0):
                print('    ',row[row_count],end=' ')
                print("\n")
                row_count+=1
        
        

                
                
        
