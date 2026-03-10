from django.db import models
from django.utils import timezone
import random
import string


def generate_pin():
    while True:
        pin = ''.join(random.choices(string.digits, k=4))
        if not Session.objects.filter(pin=pin).exists():
            return pin


class Session(models.Model):
    title        = models.CharField(max_length=200)
    subject      = models.CharField(max_length=100)
    pin          = models.CharField(max_length=4, unique=True, default=generate_pin)
    teacher_name = models.CharField(max_length=100)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def confusion_score(self):
        total = self.doubts.count()
        if not total:
            return 0
        unanswered = self.doubts.filter(is_answered=False).count()
        return round((unanswered / total) * 100, 1)

    def answered_count(self):
        return self.doubts.filter(is_answered=True).count()

    def open_count(self):
        return self.doubts.filter(is_answered=False).count()

    def online_count(self):
        cutoff = timezone.now() - timezone.timedelta(seconds=90)
        return self.presences.filter(last_seen__gte=cutoff).count()

    def __str__(self):
        return f"{self.title} [PIN: {self.pin}]"


class Doubt(models.Model):
    session      = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='doubts')
    text         = models.TextField(max_length=500)
    topic_tag    = models.CharField(max_length=80, blank=True, default='')
    votes        = models.IntegerField(default=0)
    is_answered  = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-votes', '-submitted_at']

    def __str__(self):
        return self.text[:80]


class Vote(models.Model):
    doubt     = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='vote_records')
    voter_key = models.CharField(max_length=64)

    class Meta:
        unique_together = ('doubt', 'voter_key')


class StudentPresence(models.Model):
    session   = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='presences')
    voter_key = models.CharField(max_length=64)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'voter_key')
