from rest_framework import serializers
from home.models import Person,Team
from django.contrib.auth.models import User



class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields=['team_name']
        

class PersonSerializer(serializers.ModelSerializer):
    is_adult=serializers.SerializerMethodField()
    team=TeamSerializer(read_only=True)
    class Meta:
        model=Person
        fields='__all__'


    def get_is_adult(self,obj):
        return obj.age>=22

    def validate(self,data):
        spl_chars="!@^%*()"
        if any(c in spl_chars for c in data['name']):
            raise serializers.ValidationError("name should not contain special characters")
        if data['age']<18:
            raise serializers.ValidationError("age should be > 18")
        
        return data
    
# class PersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = '__all__'





#------------------authetication
#regiaterserializer


class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("username already exists")
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("email already exists")
        return data
            
    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

#login serializer

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
