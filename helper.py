import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        myfile = open("test.txt", "a")
        myfile.write('%s: \t %0.3f s\n' % (f.__name__, time2-time1))
        myfile.close()
        return ret
    return wrap