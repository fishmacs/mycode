SETUP = 'counter = 0'

LOOP_IF = """
counter += 1
"""

LOOP_EXCEPT = """
try:
    counter += 1
except:
    pass
"""


if __name__ == '__main__':
    import timeit
    if_time = timeit.Timer(LOOP_IF, setup=SETUP)
    except_time = timeit.Timer(LOOP_EXCEPT, setup=SETUP)
    print('using if statement: {}'.format(min(if_time.repeat(number=10 ** 7))))
    print('using exception: {}'.format(min(except_time.repeat(number=10 ** 7))))
