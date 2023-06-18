from serializers.base_serializer import BaseSerializer


class UserSerializer(BaseSerializer):
    fields = ('id', 'email')
