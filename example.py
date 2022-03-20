if __name__ == '__main__':
    from PythonOutputRedirect import StdoutRedirect

    f0 = StdoutRedirect('log0.txt')
    print('in')
    f0.__exit__(None, None, None)
    print('out')
    with StdoutRedirect('log1.txt') as f1:
        print('in in in')
    print('out out out')
