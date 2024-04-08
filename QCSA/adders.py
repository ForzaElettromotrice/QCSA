from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


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
        :return: the circuit representing the Quantum Adder
        """
        pass


class ThapliyalNoCarry(Adder):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder without carry-in qubit
    """

    def build(self, n: int) -> QuantumCircuit:
        # TODO
        pass


class ThapliyalWithCarry(Adder):
    """
    The Himanshu Thapliyal and Nagarajan Ranganathan quantum adder with carry-in qubit
    """

    def build(self, n: int) -> QuantumCircuit:
        # TODO
        pass
