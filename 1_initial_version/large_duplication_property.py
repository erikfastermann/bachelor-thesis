from pprint import pprint

BOTTOM = 'bottom'

def P_bottom(E):
    P = {}
    for a, rk in E.items():
        if rk == 0:
            l = a
        else:
            l = (a,) + (BOTTOM,) * rk
        P[l] = [(BOTTOM, set(), 1)]
    return P

class TrimWTGh:
    def __init__(self, Q, E, F, P_wt):
        # TODO: Check correctness.

        self.Q = Q.union({BOTTOM})
        self.E = E
        self.F = F
        self.P_wt = P_wt

    def label(self, t, w):
        if w == ():
            if isinstance(t, tuple):
                return t[0]
            else:
                return t

        i = w[0]
        if not isinstance(t, tuple) or i >= len(t):
            return None
        return self.label(t[i], w[1:])

    def pos(self, t):
        if t in self.Q or isinstance(t, str):
            # State or letter with rank zero
            return {()}

        out = {()}
        for index, subtree in enumerate(t[1:]):
            pos_ti = self.pos(subtree)
            for w in pos_ti:
                i_w = (index + 1,) + w
                out.add(i_w)
        return out

    def pos_with_labels(self, t, labels):
        out = set()
        for w in self.pos(t):
            if self.label(t, w) in labels:
                out.add(w)
        return out

    def edges(self):
        edges = {}
        for l, q_E_wt in self.P_wt.items():
            for (q, _, _) in q_E_wt:
                for q_prime in self.Q:
                    if self.pos_with_labels(l, {q_prime}) != set():
                        if q_prime not in edges:
                            edges[q_prime] = set()
                        edges[q_prime].add(q)
        return edges

    def _has_path(self, edges, visited, current_q, end_q):
        if current_q in visited:
            return False
        visited.add(current_q)

        if current_q not in edges:
            return False

        for next_q in edges[current_q]:
            if next_q == end_q:
                return True
            if self._has_path(edges, visited, next_q, end_q):
                return True

        return False

    def large_duplication_property(self):
        edges = self.edges()

        for (l, q_E_wt) in self.P_wt.items():
            for (q, E, _) in q_E_wt:
                for u, v in E:
                    l_u = self.label(l, u)
                    l_v = self.label(l, v)
                    if l_u != BOTTOM and l_v == BOTTOM:
                        for q_prime in self.Q - {BOTTOM}:
                            has_cycle = self._has_path(edges, set(), q_prime, q_prime)
                            has_path = self._has_path(edges, set(), q_prime, l_u)
                            if has_cycle and has_path:
                                return {
                                    'production': (l, q, E),
                                    'equality_constraint': (u, v),
                                    'l_u': l_u,
                                    'q_prime': q_prime
                                }
        return None

# ---

# Example 4:
Q = {'q', 'qf'}
E = {'a': 0, 'y': 1, 'd': 3}
F = {'q': 0, BOTTOM: 0, 'qf': 1}
P_wt = {
    'a': [('q', set(), 1)],
    ('y', 'q'): [('q', set(), 2)],
    ('d', 'q', ('y', BOTTOM), 'q'): [('qf', {(((1,), (2, 1)))}, 1)],
    'a': [(BOTTOM, set(), 1)],
    ('y', BOTTOM): [(BOTTOM, set(), 1)],
    ('d', BOTTOM, BOTTOM, BOTTOM): [(BOTTOM, set(), 1)],
}

G = TrimWTGh(Q, E, F, P_wt)
pprint(G.edges())
pprint(G.large_duplication_property())
print('---')

# Example 16:
Q = {'q0', 'q_', 'qf'}
E = {'a': 0, 'y': 1, 'o': 2, 'y1': 1, 'y2': 1}
F = {'q0': 0, 'q_': 0, BOTTOM: 0, 'qf': 1}
P_wt = {
    'a': [('q0', set(), 1)],
    ('y', 'q0'): [('q0', set(), 1)],
    ('o', 'q0', BOTTOM): [('q_', {((1,), (2,))}, 2)],
    ('y1', 'q_'): [('q_', set(), 2)],
    ('y2', 'q_'): [('q_', set(), 2)],
    ('o', 'q_', 'q0'): [('qf', set(), 2)],
}
P_wt.update(P_bottom(E))

G = TrimWTGh(Q, E, F, P_wt)
pprint(G.edges())
pprint(G.large_duplication_property())
