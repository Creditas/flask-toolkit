from marshmallow import Schema


class Representer(Schema):

    def render(self, data, wrapper=None):
        wrapper = wrapper or getattr(self.Meta, 'wrapper', 'data')

        if wrapper is None:
            raise NotImplementedError('Wrapper not Implementend')

        response = {
            wrapper: self.dump(data).data
        }
        return response
