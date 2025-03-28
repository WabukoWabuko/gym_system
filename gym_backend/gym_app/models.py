from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    membership_id = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CheckIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    checkout_time = models.DateTimeField(null=True, blank=True)  # Added
    synced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} - {self.timestamp}"
