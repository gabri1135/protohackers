from abc import ABC, abstractmethod


class Cipher(ABC):
    @abstractmethod
    def encode(self, plaintext: bytes) -> bytes:
        pass

    @abstractmethod
    def decode(self, ciphertext: bytes) -> bytes:
        pass


class ReverseBits(Cipher):
    def encode(self, plaintext: bytes) -> bytes:
        return bytes([int("{:08b}".format(b)[::-1], 2) for b in plaintext])

    def decode(self, ciphertext: bytes) -> bytes:
        return self.encode(ciphertext)


class Xor(Cipher):
    def __init__(self, N: int) -> None:
        self.N = N % 256

    def encode(self, plaintext: bytes) -> bytes:
        return bytes([(b ^ self.N) for b in plaintext])

    def decode(self, ciphertext: bytes) -> bytes:
        return self.encode(ciphertext)


class XorPos(Cipher):
    def __init__(self) -> None:
        self.encPos = 0
        self.decPos = 0

    def encode(self, plaintext: bytes) -> bytes:
        ciphertext = [(b ^ pos) % 256 for pos,
                      b in enumerate(plaintext, self.encPos)]
        self.encPos += len(plaintext)
        return bytes(ciphertext)

    def decode(self, ciphertext: bytes) -> bytes:
        plaintext = [(b ^ pos) % 256 for pos,
                     b in enumerate(ciphertext, self.decPos)]
        self.decPos += len(ciphertext)
        return bytes(plaintext)


class Add(Cipher):
    def __init__(self, N: int) -> None:
        self.N = N % 256

    def encode(self, plaintext: bytes) -> bytes:
        return bytes([(b+self.N) % 256 for b in plaintext])

    def decode(self, ciphertext: bytes) -> bytes:
        return bytes([(b-self.N) % 256 for b in ciphertext])


class AddPos(Cipher):
    def __init__(self) -> None:
        self.encPos = 0
        self.decPos = 0

    def encode(self, plaintext: bytes) -> bytes:
        ciphertext = [(b + pos) % 256 for pos,
                      b in enumerate(plaintext, self.encPos)]
        self.encPos += len(plaintext)
        return bytes(ciphertext)

    def decode(self, ciphertext: bytes) -> bytes:
        plaintext = [(b - pos) % 256 for pos,
                     b in enumerate(ciphertext, self.decPos)]
        self.decPos += len(ciphertext)
        return bytes(plaintext)
