from abc import ABC, abstractmethod

from qiskit import QuantumCircuit, QuantumRegister

from QCSA import merge_circuit
from QCSA.exceptions import IllegalOperandsSize, IllegalStringFormat
from QCSA.gates import Peres, TR


# Considerare se fare qualcosa in merito al "carry-in" perché potrebbe causare dei problemi nel QCSA
# Magari fare 2 tipi di Adder, quelli con carry-in e quelli senza.


class Adder(ABC):
    """
    Abstract class representing a generic adder
    """

    @abstractmethod
    def build(self, n: int) -> QuantumCircuit:
        """
        This function builds the adder based on the size of the operands
        :param n: the size of the two operands
        :return: a :class:`QuantumCircuit` representing the Quantum Adder
        """
        pass


class AdderNoCarry(Adder, ABC):
    @abstractmethod
    def initialize(self, a: str, b: str) -> QuantumCircuit:
        """
        This function initializes the two operands based on the strings passed as input.
        The strings represent binary numbers and their length must match the size of the operands.

        :param a: A string representing the first binary number.
        :param b: A string representing the second binary number.
        :return: A QuantumCircuit with the initialized operands.
        """
        pass


class AdderWithCarry(Adder, ABC):
    """
        Abstract class representing a generic adder with carry in
    """

    @abstractmethod
    def initialize(self, Cin: str, a: str, b: str) -> QuantumCircuit:
        """
        This function initializes the two operands based on the strings passed as input.
        The strings represent binary numbers and their length must match the size of the operands.

        :param Cin: A string representing the carry in. '0' or '1'.
        :param a: A string representing the first binary number.
        :param b: A string representing the second binary number.
        :return: A QuantumCircuit with the initialized operands.
        """
        pass


class Thapliyal(AdderNoCarry):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder without carry-in qubit
    """

    def __init__(self) -> None:
        """
        Initialize the adder
        """
        self.a: QuantumRegister | None = None
        self.b: QuantumRegister | None = None
        self.z: QuantumRegister = QuantumRegister(1, "z")
        self.circ = QuantumCircuit(name = "Thapliyal Adder")
        self.n = 0

    def build(self, n: int) -> QuantumCircuit:
        if n < 2:
            raise IllegalOperandsSize(f"The size of the operands must be >= 2, given {n}")
        self.n = n
        self.a = QuantumRegister(n, "a")
        self.b = QuantumRegister(n, "b")
        self.circ.add_register(self.a, self.b, self.z)

        self.__1_6()
        self.__2()
        self.__3()
        self.__4()
        self.__5()
        self.__1_6()

        return self.circ

    def initialize(self, a: str, b: str) -> QuantumCircuit:
        if len(a) != self.n or len(b) != self.n:
            raise IllegalStringFormat(f"The string \"{a}\" or \"{b}\" doesn't match the len of the operand! {len(a)} != {self.n} or {len(b)} != {self.n}")

        circ = QuantumCircuit(self.a, self.b, self.z, name = "Thapliyal Adder")
        for i, v in enumerate(a[::-1]):
            if v == "1":
                circ.x(self.a[i])

        for i, v in enumerate(b[::-1]):
            if v == "1":
                circ.x(self.b[i])

        merge_circuit(circ, self.circ)

        self.circ = circ

        return self.circ

    def __1_6(self) -> None:
        """
        First and sixth step of the Thapliyal Algorithm
        """
        for i in range(1, self.n):
            self.circ.cx(self.a[i], self.b[i])

    def __2(self) -> None:
        """
        Second step of the Thapliyal Algorithm
        """
        self.circ.cx(self.a[-1], self.z)

        for i in range(self.n - 2, 0, -1):
            self.circ.cx(self.a[i], self.a[i + 1])

    def __3(self) -> None:
        """
        Third step of the Thapliyal Algorithm
        """
        for i in range(1, self.n):
            self.circ.ccx(self.a[i - 1], self.b[i - 1], self.a[i])

    def __4(self) -> None:
        """
        Fourth step of the Thapliyal Algorithm
        """
        self.circ.append(Peres(), [self.a[-1], self.b[-1], self.z[0]])
        for i in range(self.n - 2, -1, -1):
            self.circ.append(Peres(), [self.a[i], self.b[i], self.a[i + 1]])

    def __5(self) -> None:
        """
        Fifth step of the Thapliyal Algorithm
        """
        for i in range(1, self.n - 1):
            self.circ.cx(self.a[i], self.a[i + 1])


class ThapliyalWithCarry(AdderWithCarry):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder with carry-in qubit
    """

    def __init__(self) -> None:
        """
        Initialize the adder
        """
        self.c: QuantumRegister = QuantumRegister(1, "Cin")
        self.a: QuantumRegister | None = None
        self.b: QuantumRegister | None = None
        self.z: QuantumRegister = QuantumRegister(1, "z")
        self.circ = QuantumCircuit(name = "Thapliyal Adder With Carry in")
        self.n = 0

    def build(self, n: int) -> QuantumCircuit:
        if n < 2:
            raise IllegalOperandsSize(f"The size of the operands must be >= 2, given {n}")
        self.n = n
        self.a = QuantumRegister(n, "a")
        self.b = QuantumRegister(n, "b")
        self.circ.add_register(self.c, self.a, self.b, self.z)

        self.__1_6()
        self.__2()
        self.__3()
        self.__4()
        self.__5()
        self.__1_6()

        return self.circ

    def initialize(self, Cin: str, a: str, b: str) -> QuantumCircuit:
        if len(a) != self.n or len(b) != self.n:
            raise IllegalStringFormat(f"The string \"{a}\" or \"{b}\" doesn't match the len of the operand! {len(a)} != {self.n} or {len(b)} != {self.n}")
        elif Cin != '0' and Cin != '1':
            raise IllegalStringFormat(f"The Cin must be '0' or '1' not {Cin}")

        for i in a:
            if i != '0' and i != '1':
                raise IllegalStringFormat(f"The string a must contain only '0' or '1' not {i}")
        for i in b:
            if i != '0' and i != '1':
                raise IllegalStringFormat(f"The string b must contain only '0' or '1' not {i}")

        circ = QuantumCircuit(self.c, self.a, self.b, self.z, name = "Thapliyal Adder With Carry in")

        if Cin == '1':
            circ.x(self.c)

        for i, v in enumerate(a[::-1]):
            if v == "1":
                circ.x(self.a[i])

        for i, v in enumerate(b[::-1]):
            if v == "1":
                circ.x(self.b[i])

        merge_circuit(circ, self.circ)

        self.circ = circ

        return self.circ

    def __1_6(self) -> None:
        """
        First and sixth step of the Thapliyal Algorithm
        """
        for i in range(self.n):
            self.circ.cx(self.a[i], self.b[i])

    def __2(self) -> None:
        """
        Second step of the Thapliyal Algorithm
        """
        self.circ.cx(self.a[0], self.c[0])
        for i in range(1, self.n):
            self.circ.cx(self.a[i], self.a[i - 1])

        self.circ.cx(self.a[self.n - 1], self.z)

    def __3(self) -> None:
        """
        Third step of the Thapliyal Algorithm
        """
        self.circ.ccx(self.c[0], self.b[0], self.a[0])
        for i in range(self.n - 2):
            self.circ.ccx(self.a[i], self.b[i + 1], self.a[i + 1])

        self.circ.append(Peres(), [self.a[self.n - 2], self.b[self.n - 1], self.z[0]])

        for i in range(self.n - 1):
            self.circ.x(self.b[i])

    def __4(self) -> None:
        """
        Fourth step of the Thapliyal Algorithm
        """
        for i in range(self.n - 3, -1, -1):
            self.circ.append(TR(), [self.a[i], self.b[i + 1], self.a[i + 1]])
        self.circ.append(TR(), [self.c[0], self.b[0], self.a[0]])

        for i in range(self.n - 1):
            self.circ.x(self.b[i])

    def __5(self) -> None:
        """
        Fifth step of the Thapliyal Algorithm
        """
        for i in range(self.n - 1, 0, -1):
            self.circ.cx(self.a[i], self.a[i - 1])
        self.circ.cx(self.a[0], self.c[0])
