from csp import min_conflicts, backtracking_search, AC3, CSP, forward_checking
from search import depth_first_graph_search
from collections import defaultdict

def Schedule():
    """Return an instance of the Schedule problem."""
    Profs = 'Plantinga Norman Schuurman Adams'.split()
    Courses = '108 112 212 214 336 384 395'.split()
    Times = '9mwf 1030mwf 1130mwf 1030tth 130tth'.split()
    Rooms = 'nh253 sb384'.split()
    variables = list(Courses)
    domainsList = []
    for x in Profs:
        for y in Times:
            for z in Rooms:
                domainsList.append(x + "," + y + "," + z)
    domains = {}
    for var in variables:
        domains[var] = domainsList

    neighbors = defaultdict(list)
    for type in [Courses, domainsList]:
        for A in type:
            for B in type:
                if A != B:
                    if B not in neighbors[A]:
                        neighbors[A].append(B)
                    if A not in neighbors[B]:
                        neighbors[B].append(A)

    def dbg(A, a, B, b):
        print(A, a, B, b)
        s = class_constraint(A, a, B, b)
        print(s)
        return s

    def class_constraint(A, a, B, b):
        al = a.split(',')
        bl = b.split(',')

        ok = True

        if a == 'Norman,9mwf,sb384' and b == 'Adams,130tth,sb384':
            print('hi')

        # Prof the same, ensure time is different
        if al[0] == bl[0] and al[1] == bl[1]:
            ok = False
        # Time the same, ensure room and prof are different
        if al[1] == bl[1]:
            if al[2] == bl[2] or al[0] == bl[0]:
                ok = False

        # Room the same, ensure time is different
        if al[2] == bl[2] and al[1] == bl[1]:
            ok = False

        if al[0] == 'Plantinga' and A not in ('212', '395'):
            return False
        if al[0] == 'Norman' and A not in ('336', '108'):
            return False
        if al[0] == 'Schuurman' and A not in ('384', '108'):
            return False
        if al[0] == 'Adams' and A not in ('112', '214'):
            return False
        if bl[0] == 'Plantinga' and B not in ('212', '395'):
            return False
        if bl[0] == 'Norman' and B not in ('336', '108'):
            return False
        if bl[0] == 'Schuurman' and B not in ('384', '108'):
            return False
        if bl[0] == 'Adams' and B not in ('112', '214'):
            return False

        return ok
    return CSP(variables, domains, neighbors, class_constraint)


problem = Schedule()

#solution = backtracking_search(problem, inference=forward_checking)
solution = min_conflicts(problem)

print(solution)
