from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate
from qiskit.circuit.library import SXdgGate

csxdg = CSxdgGate = SXdgGate().control()


class Peres(Gate):
    """
    The Peres gate
    """

    def __init__(self):
        super().__init__('Peres', 3, [], label = "Peres")

    def _define(self):
        a = QuantumRegister(1, "A")
        b = QuantumRegister(1, "B")
        c = QuantumRegister(1, "C")

        qc = QuantumCircuit(a, b, c, name = self.name)

        qc.append(CSxdgGate, [a, c])
        qc.append(CSxdgGate, [b, c])
        qc.cx(a, b)
        qc.csx(b, c)

        self.definition = qc
