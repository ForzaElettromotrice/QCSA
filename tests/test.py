from mqt import ddsim
from qiskit import QuantumCircuit

from QCSA.adders import HaiShengLi


def simulate(c: QuantumCircuit) -> dict[str:int]:
    backend = ddsim.DDSIMProvider().get_backend("qasm_simulator")

    job = backend.run(c)
    result = job.result()

    out: dict[str:int] = result.get_counts(c)

    print(out)
    return out


if __name__ == '__main__':
    adder = HaiShengLi()
    adder.build(5, "a", "b", "z")

    circ = adder.initialize("00001", "00001")

    circ.measure_all()
    print(circ.draw("latex_source"), file = open("out.tex", "w"))
    print(circ.draw())

    out = simulate(circ)
