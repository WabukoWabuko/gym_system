from rest_framework import serializers
from .models import Member, Schedule, BlogPost, CheckIn

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class CheckInSerializer(serializers.ModelSerializer):
    member_id = serializers.CharField(write_only=True)
    member = serializers.CharField(source='member.membership_id', read_only=True)

    class Meta:
        model = CheckIn
        fields = ['id', 'member', 'member_id', 'timestamp', 'checkout_time', 'synced']
        read_only_fields = ['id', 'timestamp', 'member']

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        try:
            member = Member.objects.get(membership_id=member_id)
            checkin = CheckIn.objects.create(member=member, **validated_data)
            return checkin
        except Member.DoesNotExist:
            raise serializers.ValidationError({"member_id": "Member with this ID does not exist."})
