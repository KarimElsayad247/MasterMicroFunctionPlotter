from unittest import TestCase, main
import plotter
import sympy as sym


class PlotterTest(TestCase):

    def test_sympy_expression_parsing(self):
        self.assertEqual(sym.parse_expr("3**3", evaluate=False), plotter.parse_function("3**3"),
                         "Successfully parses and evaluates a valid expression")

        self.assertEqual(sym.parse_expr("3**3", evaluate=False), plotter.parse_function("3^3"),
                         "Successfully transforms xor into power operator")

        self.assertEqual(sym.parse_expr("6**0", evaluate=False), plotter.parse_function("6^0"),
                         "Raising to the power of zero is working correctly")

        self.assertEqual(sym.parse_expr("x**2", evaluate=False), plotter.parse_function("x^2"),
                         "Successfully parses a string containing symbolic variable")


if __name__ == '__main__':
    main()
