from . import Singleton


class Storage(metaclass=Singleton):
    instance = None

    def setup_instance(self, instance):
        self.instance = instance

    @property
    def session(self):
        return self.instance.session
