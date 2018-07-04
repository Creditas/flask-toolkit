class ChoiceMixin:

    @classmethod
    def get_choices(cls):
        return [choice.value for choice in cls]
