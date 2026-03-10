"""
Management command to seed a realistic demo session.
Usage: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from classsync.models import Session, Doubt


class Command(BaseCommand):
    help = 'Seeds a demo ClassSync session with realistic sample data for hackathon demos.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding demo session...')

        # Create demo session with a fixed PIN for easy demo
        Session.objects.filter(pin='1234').delete()
        session = Session.objects.create(
            title='Introduction to Python — Week 4',
            subject='Computer Science',
            teacher_name='Ms. Johnson',
            pin='1234',
            is_active=True,
        )

        doubts_data = [
            ('What exactly is a Python closure and why would I use it?', 'closures', 12),
            ('What is the difference between a list and a tuple? When should I use each?', 'lists', 8),
            ('How does the Django ORM actually relate to SQL under the hood?', 'orm', 7),
            ('I don\'t understand how *args and **kwargs work in functions.', 'functions', 6),
            ('What does "self" mean in a class method? Why do we always need it?', 'oop', 5),
            ('Can you explain list comprehensions with a real example?', 'lists', 4),
            ('What is a decorator and how do you write one from scratch?', 'decorators', 4),
            ('How do I handle exceptions properly? When should I use try/except?', 'exceptions', 3),
            ('What is the difference between == and "is" in Python?', 'basics', 3),
            ('How does Django know which view to call for each URL?', 'django', 2),
            ('What is a virtual environment and do I always need one?', 'setup', 1),
            ('How do I read a file in Python and handle errors if it doesn\'t exist?', 'fileio', 1),
        ]

        for i, (text, tag, votes) in enumerate(doubts_data):
            Doubt.objects.create(
                session=session,
                text=text,
                topic_tag=tag,
                votes=votes,
                is_answered=(i >= 10),  # last 2 are "answered"
            )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Demo session created!'
            f'\n   PIN:      1234'
            f'\n   Doubts:   {len(doubts_data)}'
            f'\n   Teacher:  {session.teacher_name}'
            f'\n\n👉 Teacher dashboard: http://127.0.0.1:8000/session/1234/teacher/'
            f'\n👉 Student join:       http://127.0.0.1:8000/join/'
            f'\n👉 Analytics:          http://127.0.0.1:8000/session/1234/analytics/'
        ))
