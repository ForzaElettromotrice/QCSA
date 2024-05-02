from qiskit import QuantumCircuit


def merge_circuit(circ1: QuantumCircuit, circ2: QuantumCircuit) -> None:
    """
    Merge two instances of :class:`QuantumCircuit` into circ1.
    The quantum registers named in circ2 must also be present in circ1.
    :param circ1: the :class:`QuantumCircuit` where the final circuit will be
    :param circ2: the :class:`QuantumCircuit` you want to merge
    """
    for instr, qargs, cargs in circ2.data:
        circ1.append(instr, qargs, cargs)
