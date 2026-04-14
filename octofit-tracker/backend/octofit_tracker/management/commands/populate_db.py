from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all users
        User.objects.all().delete()

        # Create Marvel and DC teams
        Team = self.get_or_create_collection('teams')
        Activity = self.get_or_create_collection('activities')
        Leaderboard = self.get_or_create_collection('leaderboard')
        Workout = self.get_or_create_collection('workouts')

        Team.delete_many({})
        Activity.delete_many({})
        Leaderboard.delete_many({})
        Workout.delete_many({})

        marvel_team = Team.insert_one({'name': 'Team Marvel'})
        dc_team = Team.insert_one({'name': 'Team DC'})

        # Create users
        users = [
            {'email': 'ironman@marvel.com', 'name': 'Iron Man', 'team': 'Team Marvel'},
            {'email': 'captainamerica@marvel.com', 'name': 'Captain America', 'team': 'Team Marvel'},
            {'email': 'spiderman@marvel.com', 'name': 'Spider-Man', 'team': 'Team Marvel'},
            {'email': 'batman@dc.com', 'name': 'Batman', 'team': 'Team DC'},
            {'email': 'superman@dc.com', 'name': 'Superman', 'team': 'Team DC'},
            {'email': 'wonderwoman@dc.com', 'name': 'Wonder Woman', 'team': 'Team DC'},
        ]
        for user in users:
            User.objects.create_user(username=user['email'], email=user['email'], password='password', first_name=user['name'], last_name=user['team'])

        # Create activities
        Activity.insert_many([
            {'user': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user': 'batman@dc.com', 'activity': 'Cycling', 'duration': 45},
        ])

        # Create leaderboard
        Leaderboard.insert_many([
            {'team': 'Team Marvel', 'points': 100},
            {'team': 'Team DC', 'points': 90},
        ])

        # Create workouts
        Workout.insert_many([
            {'name': 'Pushups', 'difficulty': 'Easy'},
            {'name': 'Pullups', 'difficulty': 'Medium'},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

    def get_or_create_collection(self, name):
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        collection = db[name]
        return collection
