from abc import ABC, abstractmethod

from qiskit import QuantumCircuit, QuantumRegister

from QCSA.exceptions import IllegalOperandsSize
from QCSA.gates import Peres


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


class ThapliyalNoCarry(Adder):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder without carry-in qubit
    """

    def __init__(self):
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
        self.circ.cx(self.z, self.a[-1])

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


class ThapliyalWithCarry(Adder):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder with carry-in qubit
    """

    def build(self, n: int) -> QuantumCircuit:
        # TODO
        pass
