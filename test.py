from unittest import TestCase, main
import plotter


class PlotterTest(TestCase):

    def test_symbolic_math(self):
        self.assertEqual(2, plotter.sum(1,1), "test runner is working")


if __name__ == '__main__':
    main()
