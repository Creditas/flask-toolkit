from marshmallow import Schema


class Representer(Schema):

    def render(self, data, wrapper=None):
        wrapper = wrapper or getattr(self.Meta, 'wrapper', 'data')

        response = {
            wrapper: self.dump(data)
        }

        return response
