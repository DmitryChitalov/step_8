import threading


class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, object, schema):
        self.new_objects.append({'object': object, 'schema': schema})

    def register_dirty(self, object, schema):
        self.dirty_objects.append({'object': object, 'schema': schema})

    def register_removed(self, object):
        self.removed_objects.append(object)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for object in self.new_objects:
            self.MapperRegistry.get_mapper(object['object']).insert(
                **object['schema'])

        self.new_objects.clear()

    def update_dirty(self):
        for object in self.dirty_objects:
            self.MapperRegistry.get_mapper(object['object']).insert(
                object['object'], **object['schema'])

        self.dirty_objects.clear()

    def delete_removed(self):
        for object in self.removed_objects:
            self.MapperRegistry.get_mapper(object).delete(object)

        self.removed_objects.clear()

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self, schema):
        UnitOfWork.get_current().register_new(self, schema)

    def mark_dirty(self, schema):
        UnitOfWork.get_current().register_dirty(self, schema)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
