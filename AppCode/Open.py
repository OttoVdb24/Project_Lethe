from subprocess import call

class CallPy(object):

    def __init__(self):
        pass
    def call_python_file(self, path):
        call(["Python3","{}".format(path)])


C = CallPy()
C.call_python_file(r'\Users\otto\Documents\1-IO\4-Project Gebruiksgericht\Repo\Project_Lethe\AppCode\PlanningApp.py')
