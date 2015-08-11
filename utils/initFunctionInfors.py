import os
import django
import sys

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import functions, track_functions, project, teams

def getFunctions(filename, year):
    function_file = open(filename, 'r')
    currentFunc = ''
    for l in function_file.readlines():
        if l.startswith('\n'):
            continue
        if l.endswith('\n'):
            l = l[:-1]
        infoList = l.split('\t')
        teamName = infoList[0][:-4]
        try:
            func = infoList[1]
        except:
            continue
        if func == '' or func == None:
            continue
        if func.endswith('\n'):
            func = func[:-1]
        print '%s | %s' % (teamName, func)
        funObjs = functions.objects.filter(function=func)
        print funObjs
        if len(funObjs) == 0:
            funObjs = functions(function=func)
        else:
            funObjs = funObjs[0]
        funObjs.save()
        try:
            teamObj = teams.objects.get(name=teamName, year=year)
            teamObj.function = funObjs
            teamObj.save()
        except:
            print '%s not exists' % teamName

def anaFuncFiles(basepath, year):
    for parentDir, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            if filename == 'answer.txt':
                fullFilename = (parentDir if parentDir.endswith('/') else parentDir + '/') + filename
                getFunctions(fullFilename, year)

if __name__ == '__main__':
    django.setup()
    anaFuncFiles('TeamFunction/team14/', '2014')
