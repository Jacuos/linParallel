from mpi4py import MPI
import sys, re, time

startTime = time.clock()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()



def main(argv):

    if rank == 0:
        f = open(argv[1],'r')
        #B = []
        A = []
        for line in f:
            x = line.split()
        # B.append(int(x[-1]))
        # A.append(x[:-1])
            A.append(x)
    else:
        A = None
        n = None
    if rank == 0:
        #numX = len(B)
        #print(B)
        n = len(A)
    n= comm.bcast(n, root=0)

    data = [[] for i in range(size)]
    perProc = int(n/size)
    if rank==0:
        x=0
        for  y in range(n):
            if y>=perProc:
                x+=1
                perProc += n/size
            data[x].append(A[y])

    data = comm.scatter(data,root=0)
    for row in range(len(data)):
        for column in range(n+1):
            data[row][column] = float(data[row][column])
    data = comm.gather(data,root=0)

    if rank == 0:
        y=0
        for thread in data:
            for row in thread:
                A[y] = row
                y+=1
        #print(A)


    if rank != 0:
        B = None
    for i in range(0,n):
        if rank == 0:
            data = [[] for i in range(size)]
            x=0
            for  y in range(n):
                if y>=perProc:
                    x+=1
                    perProc += n/size
                data[x].append(A[y])
        # Search for maximum in this column
            maxEl = abs(A[i][i])
            maxRow = i
            for k in range(i+1, n):
                if abs(A[k][i]) > maxEl:
                    maxEl = abs(A[k][i])
                    maxRow = k

        # Swap maximum row with current row (column by column)
            for k in range(i, n+1):
                tmp = A[maxRow][k]
                A[maxRow][k] = A[i][k]
                A[i][k] = tmp
            B = A[i]
    # Make all rows below this one 0 in current column

        B= comm.bcast(B, root=0)
        data = comm.scatter(data,root=0)
        if rank ==0:
            for k in range(i+1,len(data)):
                c = -data[k][i]/B[i]
                for j in range(i, n+1):
                    if i == j:
                        data[k][j] = 0
                    else:
                        data[k][j] += c * B[j]
        else:
            for k in range(len(data)):
                c = -data[k][i]/B[i]
                for j in range(i, n+1):
                    if i == j:
                        data[k][j] = 0
                    else:
                        data[k][j] += c * B[j]
        data = comm.gather(data,root=0)

        if rank == 0:
            y=0
            for thread in data:
                for row in thread:
                    A[y] = row
                    y+=1
    # Solve equation Ax=b for an upper triangular matrix A
    if rank ==0:
        x = [0 for i in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = A[i][n]/A[i][i]
            for k in range(i-1, -1, -1):
                A[k][n] -= A[k][i] * x[i]


        #print(x)
        print("Execution time: "+str(time.clock()-startTime))
if __name__ == "__main__":
    main(sys.argv)