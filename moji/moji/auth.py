class Backend(object):
    def authenticate(self,request,u=None,p=None):
        if type(u) == str and type(p) != str:
            print('t')
            return 't'
        else:
            print('f')
            return 'f'
