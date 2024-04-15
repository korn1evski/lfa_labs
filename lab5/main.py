from AbstractGrammar import AbstractGrammar
from itertools import combinations
import unittest


class TestGrammarMethods(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(['S', 'A', 'B', 'C', 'D'], ['a', 'b'], {
            'S': ['aB', 'bA', 'A'],
            'A': ['B', 'AS', 'bBAB', 'b'],
            'B': ['b', 'bS', 'aD', 'ε'],
            'C': ['Ba'],
            'D': ['AA']
        }, 'S')

    def test_start_removal(self):
        self.grammar.start_removal()
        for prod in self.grammar.P.values():
            self.assertNotIn(self.grammar.S, prod)

    def test_rm_null_productions(self):
        self.grammar.rm_null_productions()
        for prods in self.grammar.P.values():
            self.assertNotIn('ε', prods)

    def test_rm_unit_productions(self):
        self.grammar.rm_unit_productions()
        for key, prods in self.grammar.P.items():
            for prod in prods:
                self.assertFalse(len(prod) == 1 and prod.isupper())

    def test_rm_inaccessible_symb(self):
        self.grammar.Vn.append('Z')
        self.grammar.rm_inaccessible_symb()
        self.assertNotIn('Z', self.grammar.Vn)

    def test_repl_tem_with_non(self):
        self.grammar.repl_tem_with_non()
        for prods in self.grammar.P.values():
            for prod in prods:
                if len(prod) > 1:
                    self.assertTrue(all(char in self.grammar.Vn for char in prod))

    def test_reduce_pr_length(self):
        self.grammar.repl_tem_with_non()
        self.grammar.reduce_pr_length()
        for prods in self.grammar.P.values():
            for prod in prods:
                self.assertTrue(len(prod) <= 2)

    def test_grammar_print(self):
        self.grammar.cfg_to_cnf()
        self.grammar.print_grammar()


class Grammar(AbstractGrammar):
    def cfg_to_cnf(self):
        self.start_removal()
        self.rm_null_productions()
        self.rm_unit_productions()
        self.rm_inaccessible_symb()
        self.repl_tem_with_non()
        self.reduce_pr_length()

    def start_removal(self):
        try:
            for value in self.P.values():
                for production in value:
                    for character in production:
                        if character == self.S:
                            raise BreakAll
        except:
            new_P = {'Q': [self.S]}
            new_P.update(self.P)
            self.P = new_P
            self.S = 'Q'
            self.Vn.append(self.S)

    def create_new_productions(self, production, character):
        results = []
        for i in range(len(production)):
            if production[i] == character:
                new_production = production[:i] + production[i+1:]
                results.append(new_production)
        return results

    def rm_null_productions(self):
        null_prods = {key for key, prods in self.P.items() if 'ε' in prods}
        new_P = {}

        # Remove the epsilon productions directly
        for key in self.P:
            new_P[key] = [prod for prod in self.P[key] if prod != 'ε']

        # For productions that contain non-terminals which can be null,
        # we need to add productions with these non-terminals removed
        for key, prods in new_P.items():
            for prod in prods:
                if set(prod).intersection(null_prods):
                    # Generate all combinations of the production without the nullable non-terminals
                    indexes = [i for i, char in enumerate(prod) if char in null_prods]
                    for i in range(1, len(indexes) + 1):
                        for combo in combinations(indexes, i):
                            new_combination = list(prod)
                            for index in combo:
                                new_combination[index] = ''
                            new_combination = ''.join(new_combination)
                            if new_combination and new_combination not in new_P[key]:
                                new_P[key].append(new_combination)

        # Update the productions to the new set with ε removed
        self.P = new_P

    def rm_unit_productions(self):
        for key, value in self.P.items():
            for production in value:
                if key == production:
                    self.P[key].remove(production)
        changes = True
        while changes:
            changes = False
            for key, value in self.P.items():
                for production in value:
                    if production in self.Vn:
                        changes = True
                        self.P[key].remove(production)
                        for prod in self.P[production]:
                            if prod not in self.P[key]:
                                self.P[key].append(prod)

    def rm_inaccessible_symb(self):
        accessible = set([self.S])
        queue = [self.S]

        while queue:
            current = queue.pop(0)
            for production in self.P.get(current, []):
                for symbol in production:
                    if symbol in self.Vn and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.Vn = [nt for nt in self.Vn if nt in accessible]
        for nt in list(self.P.keys()):
            if nt not in accessible:
                del self.P[nt]


    def repl_tem_with_non(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        terminal_to_nonterminal = {}
        new_P = {}
        for key, productions in self.P.items():
            new_productions = []
            for prod in productions:
                if len(prod) > 1:
                    new_prod = ''
                    for char in prod:
                        if char in self.Vt:
                            if char not in terminal_to_nonterminal:
                                new_nt = new_nonterminal(self.Vn)
                                self.Vn.append(new_nt)
                                terminal_to_nonterminal[char] = new_nt
                                new_P[new_nt] = [char]
                            new_prod += terminal_to_nonterminal[char]
                        else:
                            new_prod += char
                    new_productions.append(new_prod)
                else:
                    new_productions.append(prod)
            new_P[key] = new_productions
        self.P.update(new_P)

    def reduce_pr_length(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        existing_binaries = {}
        new_productions_dict = {}
        for key, productions in list(self.P.items()):
            new_productions = []
            for production in productions:
                if len(production) > 2:
                    while len(production) > 2:
                        last_two = production[-2:]
                        if last_two not in existing_binaries:
                            new_nt = new_nonterminal(set(self.Vn) | set(new_productions_dict.keys()))
                            self.Vn.append(new_nt)
                            new_productions_dict[new_nt] = [last_two]
                            existing_binaries[last_two] = new_nt
                        production = production[:-2] + existing_binaries[last_two]
                    new_productions.append(production)
                else:
                    new_productions.append(production)
            self.P[key] = new_productions
        self.P.update(new_productions_dict)


class BreakAll(Exception):
    pass

if __name__ == '__main__':
    unittest.main()
