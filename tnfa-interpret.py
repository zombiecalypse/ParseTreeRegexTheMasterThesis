import copy

def consume(tnfa, start, c, i):
    low = list(reversed(start))
    high = []
    R = []
    seen = set()
    buffer = []
    while low or high:
        if not high:
            e = low.pop()
            high.append(e)
            R.extend(buffer)
            buffer = []
            continue
        state, mem = high.pop()
        if state in seen:
            continue
        seen.add(state)
        transitions = tnfa.get(state, {})
        consuming = transitions.get(c)
        if consuming:
            R.append((cons, mem))
        epsilon = transitions.get(None)
        if not epsilon: continue
        for (s, tag) in epsilon:
            if tag == '-':
                low.append((s, mem))
                continue
            if tag:
                n, side = tag
                mem = copy.deepcopy(mem)
                mem.setdefault(n, ([], []))[0 if side == 'l' else 1].append(
                    i if side == 'r' else i+1)
            high.append((s, mem))
    R.extend(buffer)
    return R

def match(regex, string):
    counter = count()

    tnfa, start, end = construct(
        regex, {}, next(counter), next(counter), counter, outer=True)

    ran = [(start, {})]
    for i, c in enumerate(string + '\0'):
        ran = consume(tnfa, ran, c, i)

    return dict(ran).get(end)
