from mqt import ddsim
from qiskit import QuantumCircuit, QuantumRegister

from QCSA import merge_circuit
from QCSA.adders import ThapliyalWithCarry
from QCSA.csa import QCSA


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
    # adder = ThapliyalWithCarry()
    #
    # adder.build(4, "Cin0", "a0", "b0", "z0")
    #
    # circ = adder.initialize("1", "1111", "1111")
    #
    # circ.measure_all()
    # print(circ.draw())
    #
    # out = simulate(circ)
    #
    # print(f"a = 1111\nb = 1111\nz = 0")
    # print()
    # parseC([key for key in out.keys()][0])

    qcsa = QCSA(8, 2)
    qcsa.initialize("00000001", "11111111", "0")
    circ = qcsa.build()
    print(circ.draw("latex_source"), file = open("out.tex", "w"))
    # print(circ.draw())

    circ.measure_all()
    result = simulate(circ)

    string = [key for key in result.keys()][0]
    b = string[-31:-29] + string[-20:-18] + string[-9:-7] + string[-4:-2]
    print(b)
