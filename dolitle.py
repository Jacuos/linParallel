
import sys, re, time

startTime = time.clock()

def main(argv):
    f = open(argv[1],'r')
    #B = []
    A = []
    for line in f:
        x = line.split()
       # B.append(int(x[-1]))
       # A.append(x[:-1])
        A.append(x)
    for row in range(len(A)):
        for column in range(len(A)+1):
            A[row][column] = float(A[row][column])
    #print(A)

    n=len(A)
    for i in range(n):
        for j in range(i+1,len(A[i])-1):
            A[i][j] = A[i][j]/A[i][i]
        for x in range(i+1,n):
            for y in range(i+1,len(A[i])-1):
                A[x][y] = A[x][y] - A[x][i]*A[i][y]

    L = [[float for r in range(n)]for e in range(n)]
    R = [[float for r in range(n)]for e in range(n)]
    for i in range(n):
        for j in range(len(A[i])-1):
            if j > i:
                L[i][j] = 0
            else:
                L[i][j] = A[i][j]
    for i in range(n):
        for j in range(len(A[i])-1):
            if j > i:
                R[i][j] = A[i][j]
            elif j == i:
                R[i][j] = 1
            else:
                R[i][j] = 0
    #print(L)
    #print(R)
    x = [float for i in range(n)]
    y = [float for i in range(n)]
    for i in range(n):
        sum =0
        for j in range(0,i):
            sum +=(L[i][j]*y[j])
        y[i] = (A[i][n] - sum)/L[i][i]

    for i in range(n-1,-1,-1):
        sum =0
        for j in range(i+1,n):
            sum +=(R[i][j] * x[j])
        x[i] = (y[i] - sum)/R[i][i]
    print(x)
    print("Execution time: "+str(time.clock()-startTime))
if __name__ == "__main__":
    main(sys.argv)