from qiskit import QuantumCircuit

from QCSA.adders import Adder, ThapliyalWithCarry, ThapliyalNoCarry


class QCSA:
    """
    This class represent a Quantum Carry Select Adder
    """

    def __init__(self, n: int, k: int = 0, first_adder: Adder = ThapliyalNoCarry(), second_adder: Adder = ThapliyalWithCarry()) -> None:
        """

        :param n: size of the operands
        :param k: size of the block
        :param first_adder: the first adder to be used in the block
        :param second_adder: the second adder to be used in the block
        """
        # FIXME: il teoria il secondo adder deve obbligatoriamente avere il carry in
        self.n = n
        self.k = k
        self.first_adder = first_adder
        self.second_adder = second_adder

    def build(self) -> QuantumCircuit:
        """
        This method build the circuit based on the parameters given (or set) in input
        :return: a :class:`QuantumCircuit` representing the :class:`QCSA`
        """
        # TODO
        pass
