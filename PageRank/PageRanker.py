import numpy as np
from scipy import linalg
from operator import itemgetter


def read_data():
    '''Reading the data from the text file and storing it into a matrix. Returns the matrix, number of nodes and list of edges'''
    file = "input.txt"
    edges = []

    M = []
    with open(file) as f:
        lines = f.readlines()
        nodes = int(lines[0])
        num_edges = int(lines[1])
        M = [[0.0 for _ in range(int(nodes))] for _ in range(int(nodes))]
        for i in range(2, num_edges+2):
            initial, dest = [int(x) for x in lines[i].split(",")]
            edges.append([initial, dest])
            M[initial - 1][dest - 1] = 1.0

    return M, nodes, edges


def outgoinglinks(M, nodes, edges):
    '''Calculating outgoing links and finding number of outgoing links'''
    hyperlinks = []
    L = np.array(M)

    for i in range(len(L[0])):
        if np.sum(L[i, :]) != 0:
            L[i, :] = L[i, :]/np.sum(L[i, :])
        else:
            print("No outgoing links for a node, exiting...")
            exit()

    for i in range(1, nodes+1):
        count = 0
        for j in edges:
            if j[0] == i:
                count = count+1
        hyperlinks.append(count)

    return hyperlinks, L


def calc_PTM(nodes, edges, hyperlinks):
    '''Calculating PTM with and without random teleportations'''
    random_prob = 0.1
    Trans_Matrix = []
    RT = []
    for i in range(nodes):
        x = []
        y = []
        for j in range(nodes):
            a = 0
            for k in edges:
                if k[0] == i+1 and k[1] == j+1:
                    a = 1
                    x.append(1/hyperlinks[i])
                    y.append((1/hyperlinks[i]) *
                             random_prob+((1-random_prob)/nodes))
                    break
            if a == 0:
                x.append(0)
                y.append(((1-random_prob)/nodes))
        Trans_Matrix.append(x)
        RT.append(y)

    return Trans_Matrix, RT


def calc_eigen_without(Trans_Matrix):
    '''Using linalg module to calculate eigen values and left eigen vectors of PTM without random teleportations
    and printing the pages sorted according to the eigenvalues'''

    eigen, leftvector = linalg.eig(a=np.array(
        Trans_Matrix), b=None, left=True, right=False, overwrite_a=False, overwrite_b=False, check_finite=False)

    ans = []
    max_value = 0
    index = 0

    for i, x in enumerate(eigen):
        if x > max_value:
            max_value = x
            index = i
    ans = leftvector[:, index]

    answer = []
    for i, x in enumerate(ans):
        answer.append([i+1, ans[i]])
    answer = sorted(answer, key=itemgetter(1), reverse=True)

    print("Principle Left Eigenvector of PTM without random teleportations:")
    for i in ans:
        print(i, end=" ")
    print("\n")

    print("Rankings:\nRank\tPage\tEigenvalue")
    i = 1
    for x in answer:
        print(i, end="\t")
        for j in x:
            print(j, end="\t")
        i = i+1
        print("\n")


def calc_eigen_with(RT):
    '''Using linalg module to calculate eigen values and left eigen vectors of PTM with random teleportations
    and printing the pages sorted according to the eigenvalues'''
    eigen, leftvector = linalg.eig(a=np.array(
        RT), b=None, left=True, right=False, overwrite_a=False, overwrite_b=False, check_finite=False)

    ans = []
    max_value = 0
    index = 0

    for i, x in enumerate(eigen):
        if x > max_value:
            max_value = x
            index = i
    ans = leftvector[:, index]

    print("Principle Left Eigenvector of PTM with random teleportations:\n")
    for i in ans:
        print(i, end=" ")
    print("\n")

    i = 1
    answer = []
    for x in ans:
        answer.append([i, ans[i-1]])
        i = i+1

    answer = sorted(answer, key=itemgetter(1), reverse=True)
    print("Rankings:\nRank\tPage\tEigenvalue")
    i = 1
    for x in answer:
        print(i, end="\t")
        for j in x:
            print(j, end="\t")
        i = i+1
        print("\n")


def power_without(nodes, Trans_Matrix):
    '''Using power iteration method to calculate eigen values and left eigen vectors of PTM without random teleportations
    and printing the pages sorted according to the eigenvalues'''

    print("Using Power iteration method")
    print("1. Without random teleportation")

    arr = [1.0 for _ in range(int(nodes))]
    leftvectorpower = np.array(arr)
    eigenpower = 0.0
    iter = 70
    for i in range(iter):
        leftvectorpower = np.matmul(leftvectorpower, Trans_Matrix)
        eigenpower = linalg.norm(leftvectorpower)
        leftvectorpower = leftvectorpower/eigenpower
    leftvectorpower = list(leftvectorpower)
    i = 1
    answer = []
    for x in leftvectorpower:
        answer.append([i, leftvectorpower[i-1]])
        i = i+1
    answer = sorted(answer, key=itemgetter(1), reverse=True)
    print("Rankings:\nRank\tPage\tEigenvalue")
    i = 1
    for x in answer:
        print(i, end="\t")
        for j in x:
            print(j, end="\t")
        i = i+1
        print("\n")


def power_with(nodes, RT):
    '''Using power iteration method to calculate eigen values and left eigen vectors of PTM with random teleportations
    and printing the pages sorted according to the eigenvalues'''
    print("2. With random teleportation")

    arr = [1.0 for _ in range(int(nodes))]
    leftvectorpower = np.array(arr)
    eigenpower = 0.0
    iter = 70
    for i in range(iter):
        leftvectorpower = np.matmul(leftvectorpower, RT)
        eigenpower = linalg.norm(leftvectorpower)
        leftvectorpower = leftvectorpower/eigenpower

    leftvectorpower = list(leftvectorpower)
    i = 1
    answer = []
    for x in leftvectorpower:
        answer.append([i, leftvectorpower[i-1]])
        i = i+1
    answer = sorted(answer, key=itemgetter(1), reverse=True)
    print("Rankings:\nRank\tPage\tEigenvalue")
    i = 1
    for x in answer:
        print(i, end="\t")
        for j in x:
            print(j, end="\t")
        i = i+1
        print("\n")


M, nodes, edges = read_data()
hyperlinks, L = outgoinglinks(M, nodes, edges)
Trans_Matrix, RT = calc_PTM(nodes, edges, hyperlinks)
calc_eigen_without(Trans_Matrix)
calc_eigen_with(RT)
power_without(nodes, Trans_Matrix)
power_with(nodes, RT)
