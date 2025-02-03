a=[3,7,4,6,10,9,8,5]
print(a[7]) 
print(len(a))

sum = 0
for l in range(0,len(a)):
    sum = sum + a[l]

avg = sum/len(a)
print(avg)