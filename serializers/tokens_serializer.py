from serializers.base_serializer import BaseSerializer


class TokenSerializer(BaseSerializer):
    fields = ("token",)
