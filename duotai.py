# coding:utf-8

class A(object):
    def __init__(self,name=''):
        self.name=name
    def tlak(self):
        pass

class B(A):
    def tlak(self):
        print('b')

class C(A):
    def tlak(self):
        print('c')

class Person(object):
    def __init__(self,name):
        self.name=name
    def get_sleeptime(self):
        return 11

class Programmer(Person):
    def __init__(self,lang,name):
        super(Programmer,self).__init__(name)
        self.lang=lang
    def get_sleeptime(self):
        return 1

if __name__=='__main__':
    a=A()
    a.tlak()

    b=B('mao')
    b.tlak()

    c=C('wang')
    c.tlak()