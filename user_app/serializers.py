from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers 
# import ModelSerializer,Serializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email','password','name')
        extra_kwargs = {
            'password' : {'write_only':True, 'min_length':5}
        }
    
    def create(self,validated_data): # override the create function
        """Create a new user with  encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type':'password'},
        trim_whitespace = False,
    )

    def validate(self,attrs):
        """ Validate and authenticate  the user"""
        email = attrs.get('email')
        password = attrs.get('password') 

        user = authenticate(
            request= self.context.get('request'),
            username = email,
            password = password,
        )

        if not user : # authentication fails
            msg = 'Unable to authenticate  with provided credentials'
            raise serializers.ValidationError(msg,code = 'authentication')

        attrs['user'] = user
        return attrs # validation function SHOULD  raise a serializers.ValidationError if necessary, or just return the validated values