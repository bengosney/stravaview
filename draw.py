import yaml
from stravaio import strava_oauth2, StravaIO
import polyline

from pprint import pprint

class Settings:
    defaultSettings = {
        'api': {
            'client_id': None,
            'client_secret': None,
        }
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


if s.settings['token'] is None:
    data = strava_oauth2(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET)
    s.settings['token'] = data
    s.save()

client = StravaIO(access_token=s.settings['token']['access_token'])
athlete = client.get_logged_in_athlete()
athlete.store_locally()

list_activities = client.get_logged_in_athlete_activities(after='last week')

# Obvious use - store all activities locally
for a in list_activities:    
    activity = client.get_activity_by_id(a.id)
    activity.store_locally()
    pprint(activity.to_dict())
    line = activity.to_dict()['map']['polyline']
    print(line)
    points = polyline.decode(line)
    pprint(points)
    break
