from serializers.base_serializer import BaseSerializer


class AdvertisementsSerializer(BaseSerializer):
    fields = ("id", "title", "owner")


class AdvertisementDetailSerializer(BaseSerializer):
    fields = "__all__"
