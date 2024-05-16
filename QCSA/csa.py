from qiskit import QuantumCircuit, QuantumRegister

from QCSA import merge_circuit
from QCSA.adders import Adder, ThapliyalWithCarry, Thapliyal, AdderWithCarry, AdderNoCarry
from QCSA.exceptions import IllegalArgument, IllegalAdder, IllegalStringFormat


class QCSA:
    """
    This class represent a Quantum Carry Select Adder
    """

    def __init__(self, n: int, k: int = 0, first_adder: Adder = Thapliyal(), second_adder: AdderWithCarry = ThapliyalWithCarry()) -> None:
        """
        :param n: size of the operands
        :param k: size of the block
        :param first_adder: the first adder to be used in the block
        :param second_adder: the second adder to be used in the block
        """
        if n % k != 0:
            raise IllegalArgument(f"Cannot divide the operand into blocks of size {k}")
        self.n = n
        self.k = k
        self.first_adder = first_adder
        self.second_adder = second_adder

        self.circ: QuantumCircuit | None = None

        self.a: str = ""
        self.b: str = ""
        self.c_in: str = ""

    def initialize(self, a: str, b: str, c_in: str):
        if len(a) != self.n or len(b) != self.n or len(c_in) != 1:
            raise IllegalStringFormat(f"The string passed doesn't match the size of the operands! ({len(a)} or {len(b)}) != {self.n} or {len(c_in)} != 1")
        self.a = a[::-1]
        self.b = b[::-1]
        self.c_in = c_in

    def build(self) -> QuantumCircuit:
        """
        This method build the circuit based on the parameters given (or set) in input
        :return: a :class:`QuantumCircuit` representing the :class:`QCSA`
        """
        if self.a == "":
            self.initialize("0" * self.n, "0" * self.n, "0")
        self.circ = QuantumCircuit(name = "Quantum Carry Select Adder")
        self.__merge("c0", "a0", "b0", "z0", self.a[:self.k][::-1], self.b[:self.k][::-1], self.c_in)
        z = self.first_adder.z

        for i in range(1, self.n // self.k):
            self.__merge(f"c{i}_0", f"a{i}_0", f"b{i}_0", f"z{i}_0", self.a[self.k * i:self.k * (i + 1)][::-1], self.b[self.k * i:self.k * (i + 1)][::-1], "0")
            self.second_adder.build(self.k, f"c{i}_1", f"a{i}_1", f"b{i}_1", f"z{i}_1")
            c = self.second_adder.initialize("1", self.a[self.k * i:self.k * (i + 1)][::-1], self.b[self.k * i:self.k * (i + 1)][::-1])
            merge_circuit(self.circ, c)
            for j in range(self.k):
                self.circ.cswap(z, self.first_adder.b[j], self.second_adder.b[j])
            self.circ.cswap(z, self.first_adder.z, self.second_adder.z)
            z = self.first_adder.z

        return self.circ

    def __merge(self, c_name: str, a_name: str, b_name: str, z_name: str, a_init: str, b_init: str, c_init: str):
        if isinstance(self.first_adder, AdderWithCarry):
            self.first_adder.build(self.k, c_name, a_name, b_name, z_name)
            c = self.first_adder.initialize(c_init, a_init, b_init)
            merge_circuit(self.circ, c)
        elif isinstance(self.first_adder, AdderNoCarry):
            self.first_adder.build(self.k, a_name, b_name, z_name)
            c = self.first_adder.initialize(a_init, b_init)
            merge_circuit(self.circ, c)
        else:
            raise IllegalAdder("This adder is invalid!")
