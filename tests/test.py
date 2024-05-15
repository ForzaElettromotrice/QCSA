from mqt import ddsim
from qiskit import QuantumCircuit, QuantumRegister

from QCSA import merge_circuit
from QCSA.adders import ThapliyalNoCarry

if __name__ == '__main__':
    # circ = QuantumCircuit()

    # a = QuantumRegister(2, "a")
    # b = QuantumRegister(2, "b")
    # z = QuantumRegister(1, "z")
    # circ.add_register(a, b, z)
    #
    # circ.x(a[0])
    # circ.x(b[0])
    #
    # merge_circuit(circ, ThapliyalNoCarry().build(2))
    #
    # print(circ.draw())
    #
    # circ.measure_all()

    # backend = ddsim.DDSIMProvider().get_backend("qasm_simulator")
    # job = backend.run(circ, shots = 10000)
    # counts = job.result().get_counts(circ)
    # print(counts)
    #
    # out = list([key for key in counts.keys()][0])
    # print("  z |    b    |    a")
    # print(out)

    print(ThapliyalNoCarry().build(8).draw())
