from qiskit import QuantumCircuit


def merge_circuit(circ1: QuantumCircuit, circ2: QuantumCircuit) -> None:
    """
    Merge two instances of :class:`QuantumCircuit` into circ1.
    :param circ1: the :class:`QuantumCircuit` where the final circuit will be
    :param circ2: the :class:`QuantumCircuit` you want to merge
    """
    for reg in circ2.qregs:
        if reg not in circ1.qregs:
            circ1.add_register(reg)

    for instr, qargs, cargs in circ2.data:
        circ1.append(instr, qargs, cargs)
