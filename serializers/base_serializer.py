class BaseSerializer:
    fields = None

    def __init__(self, query):
        self.__query = query
        self.data = None
        self.__serialize(self.__query)

    def __serialize(self, query):
        if isinstance(query, list):
            self.data = []
            for item in query:
                self.data.append(self.__serialize_data(item))
        else:
            self.data = self.__serialize_data(query)

    def __serialize_data(self, item) -> dict:
        if self.fields == '__all__':
            keys = item.__table__.columns.keys()
            return {key: getattr(item, key) for key in keys}
        else:
            return {key: getattr(item, key) for key in self.fields}
