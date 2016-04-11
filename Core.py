from threading import Thread
from helper import timing


class Core(Thread):
    def __init__(self, cid):
        super(Core, self).__init__()
        self.cid = cid
        self.scopes = {}
        self.running = False

    def __str__(self):
        return "%d: %s" % (self.cid, self.scopes)

    def add_scope(self, scope_range):
        self.scopes[scope_range] = None

    def get_scopes(self):
        temp = []
        my_copy = dict(self.scopes)
        for k, v in my_copy.items():
            if v is not None:
                temp.append(k)
        r = set()
        for k in temp:
            r.update(self.scopes.pop(k))
        return r

    def have_scopes(self):
        return bool(self.scopes)

    def need_scope(self):
        my_copy = dict(self.scopes)
        for v in my_copy.values():
            if v is None:
                return False
        return True

    def run(self):
        self.running = True
        while self.running:
            temp = None
            my_copy = dict(self.scopes)
            for scope, results in my_copy.items():
                if results is None:
                    temp = scope
                    break
            if temp:
                self.scopes[temp] = self.__handle_numbers(temp)

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    @timing
    def __handle_numbers(self, numbers):
        s = set()
        for n in numbers:
            if self.__check_number(n):
                s.add(n)
        return s

    def __check_number(self, n):
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
