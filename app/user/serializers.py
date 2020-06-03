from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # Specify the model that you want to base your model serializer from
        model = get_user_model()

        # Fiels that are gonna be converted to and from JSON when an HTTP POST
        fields = ('email', 'password', 'name')

        # Extra settings
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # This is from the Django rest-framework docs
    # Override the create function
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        # When create a new user validated_data will contain that pass
        # into the serializer which would be the JSON data that was made
        # in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # attrs: every fiel that makes up the serializer
    def validate(self, attrs):
        """Validate and authenticate the user"""

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
