from collections import defaultdict

from build.badRequest import BadRequest


class Directory:
    def __init__(self) -> None:
        self.file = FileVersion()
        self.dir = defaultdict(Directory)

    def versionDir(self):
        if self.file.version > 0:
            return f'r{self.file.version}'
        return 'DIR'

    def put(self, path, text):
        if len(path) == 0 or path == ['']:
            return self.file.put(text)

        return self.dir[path[0]].put(path[1:], text)

    def get(self, path, version):
        if len(path) == 0 or path == ['']:
            return self.file.get(version)

        return self.dir[path[0]].get(path[1:], version)

    def lista(self, path):
        lista = []
        if len(path) == 0 or path == ['']:
            for name, dir in self.dir.items():
                if dir.versionDir() == 'DIR':
                    lista.append(f'{name}/ {dir.versionDir()}')
                else:
                    lista.append(f'{name} {dir.versionDir()}')
            return lista

        return self.dir[path[0]].lista(path[1:])


class FileVersion:
    def __init__(self):
        self.texts: list[str] = ['']
        self.version: int = 0

    def put(self, data):
        if data != self.texts[-1]:
            self.texts.append(data)
            self.version += 1
        return f'r{self.version}'

    def get(self, ver):
        if 1 <= ver <= self.version or ver == -1:
            return self.texts[ver], len(self.texts[ver])
        raise BadRequest('no such revision')
