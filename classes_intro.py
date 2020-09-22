class Strategy:
    """
    Docstring: This is a class object named 'Strategy' which will create different instances based on two standard moving averages
    """

    count_strategies = 0 # This is a class attribute

    def __init__(self, class_fast_sma, class_slow_sma=9):
        print('Creating a Strategy')
        self.fast_sma = class_fast_sma
        self.slow_sma = class_slow_sma
        Strategy.count_strategies += 1

print('Running file ...')

goldencross1 = Strategy(3)
print('Fast sma: {}'.format(goldencross1.fast_sma))
print('Slow sma: {}'.format(goldencross1.slow_sma))

goldencross2 = Strategy(6, 12)
print('Fast sma: {}'.format(goldencross2.fast_sma))
print('Slow sma: {}'.format(goldencross2.slow_sma))

goldencross1.fast_sma = 4
print('New fast sma: {}'.format(goldencross1.fast_sma))

print('{} strategies created'.format(Strategy.count_strategies))