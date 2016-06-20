import sys,random

def main(argv):
    f = open(argv[1],'w')
    dim = int(argv[2])
    A = [[int for i in range(dim+1)] for j in range(dim)]
    for x in range(dim):
        for y in range(dim+1):
            A[x][y] = random.uniform(-1000,1000)
    for x in range(dim):
        for y in range(dim+1):
            f.write(str(A[x][y])+" ")
        f.write("\n")

if __name__ =="__main__":
    main(sys.argv)