import importlib


class AutoDiscover:
    """
    This class search modules from path recursively. What it does
    is actually search all the modules and run an `import_module` for each.

    :param path: `pathlib.Path` object
    :param pattern: Must be a string for search likes string.endswith(pattern)
    :return: modules list

    How to use:

        autodiscover = AutoDiscover(path=...)
        autodiscover()
    """

    def __init__(self, path, pattern=None):
        self.path = path
        self.pattern = pattern
        self.root = self.__get_dotted_full_path(path=path)

    def __call__(self):
        return self.__autodiscover(path=self.path, pattern=self.pattern)

    def __autodiscover(self, path, pattern):
        modules = []

        for obj in path.iterdir():
            if obj.name.startswith('_'):
                continue

            if (
                    obj.is_file()
                and obj.suffix == '.py'
                and obj.match(pattern or '*')
            ):
                module_name = self.__normalize_module_name(
                    module_name='.'.join(obj.parts).replace('.py', '')
                )
                modules.append(importlib.import_module(module_name))

            if obj.is_dir():
                modules.extend(self.__autodiscover(path=obj, pattern=pattern))

        return modules

    def __normalize_module_name(self, module_name):
        return module_name[module_name.find(self.root):]

    def __get_root_parts(self, path):
        def get_root_parts(path):
            parts = []
            try:
                next(path.glob('__init__.py'))
            except StopIteration:
                return parts
            parts.append(path.name)
            parts.extend(get_root_parts(path.parent))
            return parts
        return reversed(get_root_parts(path=path))

    def __get_dotted_full_path(self, path):
        return '.'.join(self.__get_root_parts(path=path))
