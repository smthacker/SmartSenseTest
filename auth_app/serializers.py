from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from auth_app.models import Education, Language, User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class UserSerializer(DynamicFieldsModelSerializer):
    education_name = serializers.ReadOnlyField()
    language_name = serializers.ReadOnlyField()
    # languages = serializers.CharField(max_length=120, required=False)
    class Meta:
        model = User
        fields = "__all__"


class UserEmailExistsSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])


class UserCreateSerializer(serializers.Serializer):
    LOGIN_TYPES = [
        (1, 'Manual'),
        (2, 'Linkedin'),
        (3, 'Google')
    ]
    TITLES = [
        ('Dr', 'Dr'),
        ('Miss', 'Miss'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Mx', 'Mx'),
        ('Prof', 'Prof'),
    ]
    title = serializers.ChoiceField(required=False, choices=TITLES, default='')
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=32, write_only=True, required=True)
    login_type = serializers.ChoiceField(default=1, choices=LOGIN_TYPES)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(allow_blank=True, read_only=True)
    LOGIN_TYPES = [
        (1, 'Manual'),
        (2, 'Linkedin'),
        (3, 'Google')
    ]
    login_type = serializers.ChoiceField(default=1, choices=LOGIN_TYPES)
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'password', 'login_type']
        # read_only_fields = ['isPaidUser',]
        extra_kwargs = {
            'password': {"write_only": True, 'required': False}
        }

    def validate(self, data):
        user_obj = None
        email = data.get('email')
        password = data.get('password')
        login_type = data.get('login_type')

        if not login_type:
            raise ValidationError("Login type not provided.")

        if not email:
            raise ValidationError("Email is required to login.")

        user = User.objects.filter(Q(email=email)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This email is not valid.")
        if login_type == 1:
            if user_obj:
                if password:
                    if not user_obj.check_password(password):
                        raise ValidationError('Incorrect credentials. Please try again.')
                else:
                    raise ValidationError('Password not provided.')
        # user_obj = authenticate(username=data['email'], password=data['password'])
        # return data
        return {'user': user_obj}