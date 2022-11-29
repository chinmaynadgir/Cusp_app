t=int(input())
for solve in range(0,t):
    def  countSetBits(n):
        count = 0
        while (n):
            count += n & 1
            n >>= 1
        return count
    
    l,k=input().split()
    l1=list()
    k1=list()
    l1.append(int(l))
    k1.append(int(k))
    for iter in range(0,t-1):
        count=0
        r=l1[t]
        while (count<k1[t]):
            count=count+countSetBits(r)
            r=r+1

        print(r-1)
    
