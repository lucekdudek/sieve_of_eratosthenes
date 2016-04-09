from Core import Core
import time


class Main:
    def __init__(self, number_of_threads, scope, parts):
        self.n = number_of_threads
        self.scope = scope
        self.parts = parts
        self.result = set()

    def __str__(self):
        return "%s" % sorted(self.result)

    def go(self):
        cores = []
        for i in range(self.n):
            cores.append(Core(i))
        for c in cores:
            c.start()
        scopes = self.get_scopes(range(2, self.scope), self.parts)
        while self.some_core_are_running(cores):
            for c in cores:
                if scopes and c.need_scope():
                    c.add_scope(tuple(scopes.pop()))
                    self.result.update(c.get_scopes())
                elif c.have_scopes():
                    self.result.update(c.get_scopes())
                else:
                    c.stop()
        for c in cores:
            c.join()

    def some_core_are_running(self, cores):
        for c in cores:
            if c.is_running():
                return True
        return False

    def get_scopes(self, scope, num):
        avg = len(scope) / float(num)
        out = []
        last = 0.0
        while last < len(scope):
            out.append(scope[int(last):int(last + avg)])
            last += avg
        return out


if __name__ == "__main__":
    start = time.time()
    m = Main(20, 1000, 100)
    m.go()
    start = time.time() - start
    print(start)
    print(m)

