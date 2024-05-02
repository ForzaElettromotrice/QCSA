from mqt import ddsim
from qiskit import QuantumCircuit

from QCSA.adders import ThapliyalWithCarry


def simulate(c: QuantumCircuit) -> dict[str:int]:
    backend = ddsim.DDSIMProvider().get_backend("qasm_simulator")

    job = backend.run(c)
    result = job.result()

    out: dict[str:int] = result.get_counts(c)

    print(out)
    return out


def parse(o: str) -> None:
    print(f"a = {o[5:]}\nb = {o[1:5]}\nz = {o[0]}")


def parseC(o: str) -> None:
    print(f"c = {o[-1]}\na = {o[5:9]}\nb = {o[1:5]}\nz = {o[0]}")


if __name__ == '__main__':
    adder = ThapliyalWithCarry()

    adder.build(4)

    circ = adder.initialize("1", "1111", "1111")

    circ.measure_all()
    print(circ.draw())

    out = simulate(circ)

    print(f"a = 1111\nb = 1111\nz = 0")
    print()
    parseC([key for key in out.keys()][0])
