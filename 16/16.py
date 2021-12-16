from itertools import islice
from math import prod
from collections.abc import Generator

with open('input') as f:
    rows = [row.strip() for row in f.readlines()]


def make_bit_gen(hex_string: str) -> Generator[str]:
    binary = bin(int(hex_string, 16))[2:]
    while len(binary) < 4 * len(hex_string):
        binary = '0' + binary
    for x in binary:
        yield x


class Packet:
    def get_bits(self, bit_gen: Generator[str], num: int) -> str:
        self.bit_length += num
        return ''.join(islice(bit_gen, num))

    def __init__(self, bit_gen: Generator[str]):
        self.bit_length = 0
        self.version = int(self.get_bits(bit_gen, 3), 2)
        self.type_ID = int(self.get_bits(bit_gen, 3), 2)

        if self.type_ID == 4:   # literal value
            bits = ''
            while True:
                next_bits = self.get_bits(bit_gen, 5)
                bits += next_bits[1:]
                if next_bits[0] == '0':
                    break
            self.data = int(bits, 2)
        else:   # operator packet
            self.length_type_ID = int(self.get_bits(bit_gen, 1), 2)
            self.data = []
            consumed_length = 0

            if self.length_type_ID == 0:
                total_length = int(self.get_bits(bit_gen, 15), 2)
                while consumed_length < total_length:
                    next_packet = Packet(bit_gen)
                    consumed_length += next_packet.bit_length
                    self.data.append(next_packet)
            elif self.length_type_ID == 1:
                num_subpackets = int(self.get_bits(bit_gen, 11), 2)
                while len(self.data) < num_subpackets:
                    next_packet = Packet(bit_gen)
                    consumed_length += next_packet.bit_length
                    self.data.append(next_packet)

            self.bit_length += consumed_length

    def version_sum(self) -> int:
        if self.type_ID == 4:
            return self.version
        return self.version + sum([subpacket.version_sum() for subpacket in self.data])

    def value(self) -> int:
        match self.type_ID:
            case 0: # sum
                return sum([subpacket.value() for subpacket in self.data])
            case 1: # product
                return prod([subpacket.value() for subpacket in self.data])
            case 2: # minimum
                return min([subpacket.value() for subpacket in self.data])
            case 3: # maximum
                return max([subpacket.value() for subpacket in self.data])
            case 4: # literal
                return self.data
            case 5: # greater-than
                return (1 if self.data[0].value() > self.data[1].value() else 0)
            case 6: # less-than
                return (1 if self.data[0].value() < self.data[1].value() else 0)
            case 7: # equal-to
                return (1 if self.data[0].value() == self.data[1].value() else 0)

    def __len__(self):
        return self.bit_length


for row in rows:
    print('Hex:', (f'{row[:60]}...{row[-5:]}' if len(row) > 70 else row))

    packet = Packet(make_bit_gen(row))

    print('Part 1:', packet.version_sum())
    print('Part 2:', packet.value())
