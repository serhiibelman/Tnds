
def decompose_list(A, decomposed):
    """
    Make decomposed list from A
    :decomposed: empty list []
    :A: matrix or list of lists
        [[[1, 2, 3], [4, 5, 6]], [7, 8, 9]]
    :return: list of 1 demension arrays
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    for sub in A:
        if type(sub) == list:
            if all([isinstance(x, list) for x in sub]):
                decompose_list(sub, decomposed)
            else:
                decomposed.append(sub)
        else:
            decomposed.append(A)
            return


def matrix_prod(matrix: list):
    """
    Count sum of products of matrix
    [[1, 2, 3],
     [1, 2, 3]]
    => 1*1 + 2*2 + 3*3
    :return: int
    """
    s = 0
    for k in range(len(matrix[0])):
        d = 1
        for i in range(len(matrix)):
            d *= matrix[i][k]
        s += d
    return s


def sum_products(array: list, *args: list):
    """
    Takes array if its 1 dimension array then return sum
    of elemets
    If more then one dimension, then return sum of 
    products of elements
    """
    array_ismatrix = all(isinstance(elem, list) for elem in array)
    if not array_ismatrix and not args:
        return sum(array)
    
    decomp_array = []
    decompose_list(array, decomp_array)
    if args:
        decomp_args = []
        decompose_list(args, decomp_args)
        decomp_array.extend(decomp_args)
    return matrix_prod(decomp_array)


def test_sum_products():
    A1 = [1, 2, 3]
    A2 = [[1, 2, 3], [1, 2, 3]]
    
    print('sum A1 ===========')
    M = sum_products(A1)
    if M == 6:
        print('>>> OK')
    else:
        print('>>> Fail')
    
    print('sum A2 ===========')
    M = sum_products(A2)
    if M == 14:
        print('>>> OK')
    else:
        print('>>> Fail')
    
    print('sum A1*A1 ===========')
    M = sum_products(A1, A1)
    if M == 14:
        print('>>> OK')
    else:
        print('>>> Fail')
    
    print('sum A1*A2 ===========')
    M = sum_products(A1, A2)
    if M == 36:
        print('>>> OK')
    else:
        print('>>> Fail')
    
    print('sum A2*A1 ===========')
    M = sum_products(A2, A1)
    if M == 36:
        print('>>> OK')
    else:
        print('>>> Fail')
    
    print('sum A2*A2 ==============')
    M = sum_products(A2, A2)
    if M == 98:
        print('>>> OK')
    else:
        print('>>> Fail')


if __name__ == '__main__':
    test_sum_products()
