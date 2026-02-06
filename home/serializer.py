from rest_framework import serializers
from home.models import Person,Team



class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields=['team_name']
        

class PersonSerializer(serializers.ModelSerializer):
    is_adult=serializers.SerializerMethodField()
    team=TeamSerializer()
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
