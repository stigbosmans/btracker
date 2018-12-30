import sys
def in_notebook():
    """
    Returns ``True`` if the module is running in IPython kernel,
    ``False`` if in IPython shell or other Python shell.
    """
    return 'ipykernel' in sys.modules


def find_intersection(first, second):
    """

    :param first: numpy array of first 1D line
    :param second: numpy array of second 1D line
    :return: tuple: element 1 = index before intersection or -1 when no intersection occured
                    element 2 = positive integer when first > second after intersection
                                negative integer when first < second after intersection
                                0 when no intersection occured
    """
    assert(len(first) == len(second))
    for i in range(len(first)-1):
        if first[i] < second[i] and first[i+1] > second[i]:
            return (i, 1)
        elif first[i] > second[i] and first[i+1] < second[i]:
            return (i, -1)
        elif first[i] == second[i]:
            if first[i+1] > second[i]:
                return (i, 1)
            else:
                return (i, -1)
    return (-1, 0)