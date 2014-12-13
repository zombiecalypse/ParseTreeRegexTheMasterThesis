from itertools import count

def add_eps(table, start, goal, tag=None):
    table.setdefault(start, {}).setdefault(None, []).append((goal, tag))
    assert (len(list(u for u, x in table[start][None] if x != '-'))
            in (0,1)), (
        "Too many non-prioritized edges in %s: %s\n\n%s" %
            (start, table[start][None], table))

def construct(expression, table, start, end, counter,
              outer=False):
    if not expression:
        return table, start, end
    (op, args) = expression
    if op == 'seq':
        iter_start = start
        iter_end = next(counter)
        for x in args:
            construct(x, table, iter_start, iter_end, counter)
            iter_start = iter_end
            iter_end = next(counter)
        add_eps(table, iter_start, end)
    if op == 'lit':
        iter_start = start
        iter_end = next(counter)
        for l in args:
            table.setdefault(iter_start, {})[l] = iter_end
            iter_start = iter_end
            iter_end = next(counter)
        add_eps(table, iter_start, end)
    if op == '*':
        up = next(counter)
        done = next(counter)
        construct(args[0], table, up, done, counter)
        add_eps(table, start, up)
        add_eps(table, done, start)
        add_eps(table, start, end, '-')
        add_eps(table, done, end, '-')
    if op == '*?':
        up = next(counter)
        construct(args[0], table, up, start, counter)
        add_eps(table, start, up, '-')
        add_eps(table, start, end)
    if op == '?':
        middle = next(counter)
        construct(args[0], table, middle, end, counter)
        add_eps(table, start, end, '-')
        add_eps(table, start, middle)
    if op == '??':
        middle = next(counter)
        construct(args[0], table, middle, end, counter)
        add_eps(table, start, middle, '-')
        add_eps(table, start, end)
    if op == 'group':
        sstart = next(counter)
        eend = next(counter)
        group, exp = args
        construct(exp, table, sstart, eend, counter)
        add_eps(table, start, sstart, (group, 'l'))
        add_eps(table, eend, end, (group, 'r'))

    if outer:
        end_of_string = next(counter)
        table.setdefault(end, {})['\0'] = end_of_string
        end = end_of_string

    return table, start, end

def seq(*e):
    return ('seq', e)

def group(i, e):
    return ('group', [i, e])

def star(e):
    return ('*', [e])

def nstar(e):
    return ('*?', [e])

def lit(e):
    return ('lit', e)

def opt(e):
    return ('?', [e])

def nopt(e):
    return ('??', [e])

