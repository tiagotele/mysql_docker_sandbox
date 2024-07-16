def same_dicts(first: list = [], second: list = [], verbose: bool = False):
    
    dicts_are_equal = True
    not_in_first = []
    not_in_second = []
    
    for e in first:
        if e not in second:
            not_in_second.append(e)
            dicts_are_equal =  False
    
    for e in second:
        if e not in first:
            not_in_first.append(e)
            dicts_are_equal =  False
    
    if not dicts_are_equal and  verbose:
        print(f"not in source = {not_in_first}")
        print(f"not in target = {not_in_second}")
    
    return dicts_are_equal

a = [{"employees": 5}, {"testtab": 3}, {"products": 0}]
b = [{"testtab": 4}, {"employees": 3}, {"products": 0}]
c = [{"testtab": 3}, {"employees": 5}, {"products": 0}] # same as a but in different order
d = [{"testtab": 3}, {"employees": 5}, {"products": 0}, {"random": 10}] 

# assert same_dicts(a, b) == False
# assert same_dicts(a, c) == True
# assert same_dicts(c, d) == False

# assert same_dicts(a, b, True) == False
# assert same_dicts(a, c, True) == True
# assert same_dicts(c, d, True) == False
