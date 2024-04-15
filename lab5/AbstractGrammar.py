class AbstractGrammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def print_grammar(self):
        print('Vn:', self.Vn)
        print('Vt:', self.Vt)
        print('Productions:')
        print('S: ', self.S)
        for key, value in self.P.items():
            print(f'{key} -- {value}')
