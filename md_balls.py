#!/usr/bin/env python
SPACES = 20


log = open('log.txt', 'w');

def Spaces(degree):
    return " " * (2 * (SPACES - degree))



def Count(signatura):
    T, degree, a, b, x, y = signatura
    if T == "SQ":
        return a * (a - 1) / 2 + a * b + a * x + a * y + b * y
    if T == "noSQ":
        return a * x + a * y + b * x

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

    if a == 0 or x == 0:
        if a == 0:
            new_signatura = ("noSQ", degree, b, 0, x, 0)
        else:
            new_signatura = ("noSQ", degree, a, 0, y, 0)
        res = NoSq(new_signatura, count)
        if res:
            new_dict_res = answer_dict_ok[new_signatura]
            if new_dict_res == "Terminal":
                answer_dict_ok[signatura] = new_dict_res
            else:
                if a==0:
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
            cur = k * (a + b) + l * (x + y) - l * k
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, l, a + b - l, k, x + y - k)
                t  = ABC(t_signatura)
                if t:
                    f_signatura = ("noSQ", degree - 1, a - l, b, x - k, y)
                    f  = ABC(f_signatura)
                    if f :
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (l, 0, k, 0))
                        return True
    for k in xrange(y+1):
        for l in xrange(a+1):
            cur = l * (x + y) + k * a - l * k
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, l, a - l, k, x + y - k)
                t  = ABC(t_signatura)
                if t:
                    f_signatura = ("noSQ", degree - 1, a - l, b, x, y - k)
                    f  = ABC(f_signatura)
                    if f :
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (l, 0, 0, k))
                        return True

    for k in xrange(x+1):
        for l in xrange(b+1):
            cur = k * (a + b) + l * x - l * k
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, l, a + b - l, k, x - k)
                t  = ABC(t_signatura)
                if t:
                    f_signatura = ("noSQ", degree - 1, a, b - l, x - k, y)
                    f  = ABC(f_signatura)
                    if f :
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (0, l, k, 0))
                        return True

    answer_set_fail.add(signatura)
    return False

'''
            a       b       x      y
a       a*(a-1)/2  a*b     a*x    a*y
b                                 b*y
'''

def Quadro(signatura, count):
    T, degree, a, b, x, y = signatura

    #if degree < DEGREE:
    #    answer_dict_ok[signatura] = "Terminal"
    #    return True

    if a==1 and b == 0:
        answer_dict_ok[signatura] = "Terminal"
        return True
    if y == 0:
        for k in xrange(0, a):
            for l in xrange(b + x + 1):
                cur = k * (k - 1) / 2 +  k * (a - k) + b * k + x * k + (a - k) * l
                if cur <= 2 ** (degree-1) and count - cur <= 2 ** (degree - 1):
                    if k == 0:
                        t_signatura = ("noSQ", degree - 1, a, 0, l, 0)
                    else:
                        t_signatura = ("SQ", degree - 1, k, a - k, b + x - l, l)
                    t = ABC(t_signatura)
                    if t:
                        f_signatura = ("SQ", degree - 1, a - k, 0, b + x - l, 0)
                        f = ABC(f_signatura)
                        if f:
                            in_b = min(b, l)
                            in_x = l - in_b
                            answer_dict_ok[signatura] = (t_signatura, f_signatura, (k, in_b, in_x, 0))
                            return True

    for k in xrange(y):
        for l in xrange(x + 1):
            cur = k * (a + b) + l * a
            if cur <= 2 ** (degree - 1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, k, l, a, b)
                t = ABC(t_signatura)
                if t:
                    f_signatura = ("SQ", degree - 1, a, b, x - l, y - k)
                    f = ABC(f_signatura)
                    if f:
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (0, 0, l, k))
                        return True

    for k in xrange(1, b + 1):
        for l in xrange(x + 1):
            cur = k * (a + y) + l * a
            if cur <= 2 ** (degree-1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("noSQ", degree - 1, k, l, a, y)
                t = ABC(t_signatura)
                if t:
                    f_signatura = ("SQ", degree - 1, a, b - k, x - l, y)
                    f = ABC(f_signatura)
                    if f:
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (0, k, l, 0))
                        return True

    for k in xrange(1, a):
        for l in xrange(x + 1):
            cur = k * (k - 1) / 2 +  k * (a - k) + b * k + x * k + y * k + (a - k) * l
            if cur <= 2 ** (degree-1) and count - cur <= 2 ** (degree - 1):
                t_signatura = ("SQ", degree - 1, k, a - k, b + y + x - l, l)
                t = ABC(t_signatura)
                if t:
                    f_signatura = ("SQ", degree - 1, a - k, b, x - l, y)
                    f = ABC(f_signatura)
                    if f:
                        answer_dict_ok[signatura] = (t_signatura, f_signatura, (k, 0, l, 0))
                        return True
    answer_set_fail.add(signatura)
    return False





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


#print Foo(2, 2)
#print Foo(3, 3)
print Foo(255, 15)
#print Foo(7, 5)
#print Foo(10, 6)
#print Foo(15, 7)
#print Foo(22, 8)
#print Foo(31, 9)
#print Foo(44, 10)
#print Foo(63, 11)
#print Foo(89, 12)
#print Foo(127, 13)
#print Foo(180, 14)
#print Foo(255, 15)
#print Foo(361, 16)
#print Foo(511, 17)
#print Foo(723, 18)
#print Foo(1023, 19)
#print Foo(1447, 20)
#print Foo(2047, 21)


#branch = open("branch.txt", "w")
#aaaaaa = "0100101110110"

#cur = ("SQ", 13, 127, 0, 0, 0)


#for i in aaaaaa:
#    print >> branch, cur, answer_dict_ok[cur]
 #   if answer_dict_ok[cur] != "Terminal":
 #       print >> branch, i
 #       if i == "1":
  #          cur = answer_dict_ok[cur][0]
  #      else:
  #          cur = answer_dict_ok[cur][1]
  #  else:
  #      break




#DEGREE = 6
#print Foo(64, 11)
#for i in sorted(answer_set_fail, key = lambda x: x[1]):
#    print i

#for k in range(2, 20):
#    print 0.5 * (  (2 ** (2 * k + 1) - 2 ** (k + 2) +  1) ** 0.5 + 1), 0.5 * ( (2 ** (2 * k + 1 ) + 1) ** 0.5 + 1 )

'''
a = [0, 1, 2, 3, 4, 7, 10, 15, 22, 31, 44, 63, 89, 127, 180, 225, 361, 511, 723, 1023, 1447, 2047]
print 2 ** -0.5
for i in xrange(0, len(a) - 1, 2):
    #print a[i], a[i + 1], a[i] / float(a[i + 1]), a[i] / float(a[i + 1] + 1), (a[i] + 1)/ float(a[i + 1] + 1)
    print (a[i] + 1)/ float(a[i + 1] + 1)

for i in xrange(1, 23):
    print a[i - 1] + 1, 2 ** (0.5 * i)
'''
#print
#for i in xrange(1, len(a) - 1, 2):
#    print a[i], a[i + 1], a[i] / float(a[i + 1]), a[i] / float(a[i + 1] + 1)

