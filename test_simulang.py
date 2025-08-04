import unittest
from symbolic_infinity import SymbolicInfinity
from simulang_parser import parse
from simulang_lexer import tokenize
from simulang_interpreter import execute, Environment

class SimuLangTests(unittest.TestCase):

    def run_simulang_code(self, code):
        tokens = tokenize(code)
        ast = parse(tokens)
        env = Environment()
        execute(ast, env)
        return env

    def test_const_assignment(self):
        code = "coeternal light := ∞;"
        env = self.run_simulang_code(code)
        self.assertIsInstance(env.get("light"), SymbolicInfinity)

    def test_var_assignment(self):
        code = "octyl time := 42;"
        env = self.run_simulang_code(code)
        self.assertEqual(env.get("time"), 42)

    def test_function_definition_and_call(self):
        code = """
        posit varnothing nabla infty ds2(): {
            print("Posit");
        }
        """
        self.run_simulang_code(code)

    def test_intertillage_loop(self):
        code = """
        posit varnothing nabla infty ds2(): {
            intertillage [2..4] -> i: {
                print(i);
            }
        }
        """
        self.run_simulang_code(code)

    def test_bifurcator(self):
        code = """
        posit varnothing nabla infty ds2(): {
            bifurcator 10[2, 3] -> a(x, y): {
                print(x);
                print(y);
            }
        }
        """
        self.run_simulang_code(code)

    def test_boundary_access(self):
        code = """
        posit varnothing nabla infty ds2(): {
            boundary [2..5] -> frame: {
                print(frame.top);
            }
        }
        """
        self.run_simulang_code(code)

    def test_delineator_block(self):
        code = """
        posit varnothing nabla infty ds2(): {
            delineator "check": {
                print("Inside delineator");
            }
        }
        """
        self.run_simulang_code(code)

    def test_recur_loop(self):
        code = """
        posit varnothing nabla infty ds2(): {
            recur ds2(3);
        }
        posit varnothing nabla infty ds2(): {
            print("Looping");
        }
        """
        self.run_simulang_code(code)

    def test_conditional_branch(self):
        code = """
        posit varnothing nabla infty ds2(): {
            octyl x := 7;
            equiangular x == 7: {
                print("Equal!");
            }
        }
        """
        self.run_simulang_code(code)

    def test_sol_block(self):
        code = """
        posit varnothing nabla infty ds2(): {
            sol day intensity 0.9 {
                print("Sunlight");
            }
            sol night duration 12.3 {
                print("Moonlight");
            }
        }
        """
        self.run_simulang_code(code)

if __name__ == '__main__':
    unittest.main()
