#!/usr/bin/env python
SPACES = 20


log = open('log1.txt', 'w');

def Spaces(degree):
    return " " * (2 * (SPACES - degree))



def Count(signatura):
    T, degree, a, b, x, y = signatura
    if T == "SQ":
        return a * (a - 1) / 2 + b * (b - 1) / 2 + x * (x - 1) / 2 + y * (y - 1) / 2 
    if T == "noSQ":
        return a * b + x * y 

answer_dict_ok = {}
answer_set_fail = set()

def ABC(signatura):
    count = Count(signatura)
    T, degree, a, b, x, y = signatura

    print Spaces(degree), count, 2 ** degree, signatura
    if count > 2 ** degree:
        print Spaces(degree), "FAIL"
        return False
    if signatura in answer_dict_ok:
        print Spaces(degree), "OK"
        return True
    if signatura in answer_set_fail:
        print Spaces(degree), "FAIL"
        return False
    if count == 1:
        answer_dict_ok[signatura] = "Terminal"
        print Spaces(degree), "OK"
        return True

    if T == "SQ":
        res = Quadro(signatura, count)
    if T == "noSQ":
        res = NoSq(signatura, count)

    print Spaces(degree), "OK" if res else "FAIL"
    #if not res:
    #    print Spaces(degree), count, 2 ** degree, signatura, "FAIL"
    '''
    if res:
        if answer_dict_ok[signatura] != "Terminal":
            if signatura in answer_dict_ok[signatura]:
                print "OLOLOLOLOLOLOLO", signatura
            if count != Count(answer_dict_ok[signatura][0]) + Count(answer_dict_ok[signatura][1]):
                print Spaces(degree), "NOOOOOOOOOOOOOOOO!!!!!!", signatura, Count(signatura), \
                    answer_dict_ok[signatura], Count(answer_dict_ok[signatura][0]), Count(answer_dict_ok[signatura][1])
            t_signatura = answer_dict_ok[signatura][0]
            f_signatura = answer_dict_ok[signatura][1]
            choise = answer_dict_ok[signatura][2]
            if sum(signatura[2:]) - sum(choise) != sum(f_signatura[2:]):
                print Spaces(degree), "FAIIIIIIL", signatura, t_signatura, f_signatura, choise
    '''
    return res


'''
   x    y
a a*x  a*y
b b*x   0
'''

def NoSq(signatura, count):
    T, degree, a, b, x, y = signatura

    #answer_dict_ok[signatura] = "Terminal"
    #return True

    if a + b <= 1:
        answer_dict_ok[signatura] = "Terminal"
        return True

    if x + y <= 1:
        answer_dict_ok[signatura] = "Terminal"
        return True

    if a == 0 or x == 0 or b==0 or y==o:
        if a == 0 or b==0:
            new_signatura = ("noSQ", degree, x, y, 0, 0)
        else:
            new_signatura = ("noSQ", degree, a, b, 0, 0)
        res = NoSq(new_signatura, count)
        if res:
            new_dict_res = answer_dict_ok[new_signatura]
            if new_dict_res == "Terminal":
                answer_dict_ok[signatura] = new_dict_res
            else:
                if a==0 or x==0:
                    answer_dict_ok[signatura] = \
                        (new_dict_res[0], new_dict_res[1],
                         (0, new_dict_res[2][0], new_dict_res[2][2], 0))
                else:
                    answer_dict_ok[signatura] = \
                        (new_dict_res[0], new_dict_res[1],
                         (new_dict_res[2][0], 0, 0, new_dict_res[2][2]))
        else:
            answer_set_fail.add(signatura)
        return res

    for k in xrange(x+1):
        for l in xrange(a+1):
            if k + l == 0:
                continue
            cur = b*l+k*y
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, l, b, k, y)
                t  = ABC(t_signatura)
                if t:
                    f_signatura = ("noSQ", degree - 1, a - l, b, x - k, y)
                    f  = ABC(f_signatura)
                    if f :
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (l, 0, k, 0))
                        return True
    for k in xrange(y+1):
        for l in xrange(b+1):
            cur = a*l+k*x
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, a, l, x, k)
                t  = ABC(t_signatura)
                if t:
                    f_signatura = ("noSQ", degree - 1, a, b-l, x, y - k)
                    f  = ABC(f_signatura)
                    if f :
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (0, l, 0, k))
                        return True


    answer_set_fail.add(signatura)
    return False


def Quadro(signatura, count):
    T, degree, a, b, x, y = signatura

    #if degree < DEGREE:
    #    answer_dict_ok[signatura] = "Terminal"
    #    return True

    if a+b+x+y==2:
        answer_dict_ok[signatura] = "Terminal"
        return True

        for k in xrange(a+1):
            for l in xrange(b + 1):
                cur = k*(a-k)+l*(b-l)
                if cur <= 2 ** (degree-1) and count - cur <= 2 ** (degree - 1):
                    if k == 0:
                        t_signatura = ("noSQ", degree - 1, k, a-k, 0, 0)
                    else:
                        t_signatura = ("noSQ", degree - 1, k, a - k, b - l, l)
                    t = ABC(t_signatura)
                    if t:
                        f_signatura = ("SQ", degree - 1, a - k, k, b - l,l)
                        f = ABC(f_signatura)
                        if f:
                            in_b = min(b, l)
                            answer_dict_ok[signatura] = (t_signatura, f_signatura, (k, in_b, 0, 0))
                            return True


def PrintAnswer(signatura, f, level, max_level):
    signatura_without_degree = (signatura[0], signatura[2], signatura[3], signatura[4], signatura[5])
    if level <= max_level:
        if answer_dict_ok[signatura] == "Terminal":
            print >> f, "|  " * level, signatura_without_degree, signatura[1], "Terminal", "\r"
        else:
            print >> f, "|  " * level, signatura_without_degree, signatura[1], answer_dict_ok[signatura][2], "\r"
            PrintAnswer(answer_dict_ok[signatura][0], f, level + 1, max_level)
            PrintAnswer(answer_dict_ok[signatura][1], f, level + 1, max_level)
            if level != max_level:
                print >> f, "|  " * level, signatura_without_degree, signatura[1], "\r"



def Foo(n, degree):
    res = ABC(("SQ", degree, n, 0, 0, 0))
    PrintAnswer(("SQ", degree, n, 0, 0, 0), log, 0, 20)
    return res



print Foo(16, 8)

