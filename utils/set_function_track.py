import os
import django
import sys
import traceback
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, tracks, functions, track_functions

def set_func_track():
    team_list = teams.objects.all()
    for team_obj in team_list:
        print team_obj.name,
        func = team_obj.function_id
        track = team_obj.track
        funcs = track_functions.objects.filter(function_id=func)
        if len(funcs) == 0:
            try:
                new_tf = track_functions(track=track, function_id=func)
                new_tf.save()
                print 'succeed'
            except:
                print 'passing'


if __name__ == '__main__':
    django.setup()
    set_func_track()