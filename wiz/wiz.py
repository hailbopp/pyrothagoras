import random
import sys
import itertools
import cProfile
from multiprocessing import Pool, Process

DEBUG = False

constants = {
    1: [3, 5, 7],
    2: [11, 13, 17],
    3: [19, 23, 29],
    4: [31, 37, 41],
    5: [43, 47, 53],
    6: [59, 61, 67],
    7: [71, 73, 79],
    8: [83, 89, 97],
    9: [101, 103, 107],
}


def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]


def get_oplist(n):
    ops = ['+', '-', '*', '/',]
    return [i for i in itertools.product(''.join(ops), repeat=n-1)]


# Recursively generate all possible paren nestings over string p
def group_parens(p, is_first_call=False):
    if len(p) == 1:
        yield p
    elif len(p) == 2:
        yield p
    else:
        # 123456
        if is_first_call:
            yield p

        if len(p) % 2 == 0:
            q = list(group_parens(p[0:len(p)/2]))
            r = list(group_parens(p[len(p)/2:len(p)]))
            for group_firsthalf in q:
                for group_secondhalf in r:
                    yield "(%s)(%s)" % (group_firsthalf, group_secondhalf)

        # 1(23456)
        # 1(2(3456))
        q = list(group_parens(p[1:]))
        for group in q:
            yield "%s(%s)" % (p[0], group)

        # 12(3456)
        # 12(3(4(56)))
        # 1234(56)
        if len(p) > 3:
            q = list(group_parens(p[1:]))
            for group in q:
                yield "%s%s" % (p[0], group)

        q = list(group_parens(p[:-1]))
        for group in q:
            yield "(%s)%s" % (group, p[-1])

        if len(p) > 3:
            q = list(group_parens(p[:-1]))
            for group in q:
                yield "%s%s" % (group, p[-1])


def is_prime(a):
    return all(a % i for i in xrange(2, a))


def is_valid_sacred_geo_number(r):
    return 2 < r < 108 and is_prime(r)


def eval_parengroup(is_prime, ops_combinations, p_group, r_dict, desired):
    # for each possible combination of operators
    for o in ops_combinations:
        new_str = ''
        op = 0
        for c in range(0, len(p_group)):
            new_str += p_group[c]
            if ((p_group[c].isdigit() and c < len(p_group) - 1 and p_group[c + 1] != ')') or (p_group[c] == ')')) \
                    and (op < len(o)):
                new_str += o[op]
                op += 1

        try:
            r = eval(new_str)

        except Exception:
            # trying to divide by 0, lol.
            continue
        if str(r) not in r_dict.keys() and is_valid_sacred_geo_number(r):
            # could possibly be an answer

            r_dict[str(r)] = new_str
            print "%s : %d" % (new_str, r)

            if r in desired:
                print "******** FOUND ANSWER ******** %s = %d" % (new_str, r)
                sys.exit(0)


def eval_permutation(group_parens, i, is_prime, ops_combinations, p, r_dict, desired):
    # for each possible grouping of parentheses
    groups = list(group_parens(''.join(p), is_first_call=True))
    # print i
    i += 1
    for p_group in groups:
        eval_parengroup(is_prime, ops_combinations, p_group, r_dict, desired)


def do_wiz():
    rolls = []
    for i in range(0, int(sys.argv[1])):
        rolls.append(random.randint(1, 6))
    rolls = map(str, rolls)

    desired = constants[int(sys.argv[2])]

    print "rolls: %s" % rolls

    permutations = list(all_perms(rolls))
    ops_combinations = get_oplist(len(rolls))

    exprs = []

    print "permutations: %d" % len(permutations)

    r_dict = {}

    i = 0

    # For each possible ordering of numbers
    for p in permutations:
        eval_permutation(group_parens, i, is_prime, ops_combinations, p, r_dict, desired)

    print "finished extraction"

    #print r_dict

