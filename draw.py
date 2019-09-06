import yaml
from stravaio import strava_oauth2, StravaIO
import polyline
import cairo
from route import Route

from pprint import pprint

class Settings:
    defaultSettings = {
        'api': {
            'client_id': None,
            'client_secret': None,
        },
        'token': None,
    }
    
    def __init__(self):
        self.file_name = 'settings.yaml'
        self.load()

    def load(self):
        try:
            with open(self.file_name, 'r') as f:
                self.settings = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.settings = self.defaultSettings
            self.save()
            
    def save(self):
        with open(self.file_name, 'w') as f:
            yaml.dump(self.settings, f)


s = Settings()

STRAVA_CLIENT_ID = s.settings['api']['client_id']
STRAVA_CLIENT_SECRET = s.settings['api']['client_secret']


if 'token' not in s.settings or s.settings['token'] is None:
    data = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    s.settings['token'] = data
    s.save()


client = StravaIO(access_token=s.settings['token']['access_token'])    
athlete = client.get_logged_in_athlete()
athlete.store_locally()

list_activities = client.get_logged_in_athlete_activities(after='1 september')

# Obvious use - store all activities locally
for a in list_activities:    
    activity = client.get_activity_by_id(a.id)
    activity.store_locally()
    #pprint(activity.to_dict())
    line = activity.to_dict()['map']['polyline']
    #print(line)
    points = polyline.decode(line)
    #pprint(points)
    if len(points) > 0:
        break


r = Route(line)
print(r)
r.normalize()
print(r)
# LAT_INDEX = 0
# LNG_INDEX = 1

# lats = [p[LAT_INDEX] for p in points]
# lngs = [p[LNG_INDEX] for p in points]

# minlat = min(lats)
# maxlat = max(lats)

# minlng = min(lngs)
# maxlng = max(lngs)

# print(lngs, f"\n\n{maxlng} - {minlng}")

# if minlat < 0:
#     adjlat = abs(minlat)
# else:
#     adjlat = 0

# if minlng < 0:
#     adjlng = abs(minlng)
# else:
#     adjlng = 0
    
width = 500
height = 500

r.scaleWithin(width, height)

def scale(OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)

    return (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


with cairo.SVGSurface("plots/route.svg", width, height) as surface:
    context = cairo.Context(surface)
    context.set_source_rgb(0.3, 0.2, 0.5)
    context.set_line_width(width / 200)
    
    for i, p in enumerate(r.points):
        y = height - p.x
        x = p.y

        if i == 0:
            context.move_to(x, y)
        
        context.line_to(x, y)

    context.stroke()
    
print(activity)
