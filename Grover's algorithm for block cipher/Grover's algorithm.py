from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
from qiskit.circuit.library import C4XGate
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate

# service = QiskitRuntimeService()
qreg_q = QuantumRegister(16, 'q')
qreg_a = QuantumRegister(1, 'a')
creg_c0 = ClassicalRegister(8, 'c0')
circuit = QuantumCircuit(qreg_q, qreg_a, creg_c0)
# # Input plain text q0 -> q7 
## If your input is 11011011 then you it'll be like this
## q7 is msb, q0 is lsb
circuit.x(qreg_q[0])
circuit.x(qreg_q[1])
# circuit.x(qreg_q[2])
circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# circuit.x(qreg_q[5])  
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])

# Quantum superposition
circuit.x(qreg_a[0])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[10])
circuit.h(qreg_q[11])
circuit.h(qreg_q[12])
circuit.h(qreg_q[13])
circuit.h(qreg_q[14])
circuit.h(qreg_q[15])
circuit.h(qreg_a[0])

#//////////////
#Round 1
#//////////////


#first Iterator
#May need more iterator in oder to find the result, just copy from here until you see "Measurement" line
# Add roundkey
circuit.cx(qreg_q[8], qreg_q[0])
circuit.cx(qreg_q[9], qreg_q[1])
circuit.cx(qreg_q[10], qreg_q[2])
circuit.cx(qreg_q[11], qreg_q[3])
circuit.cx(qreg_q[12], qreg_q[4])
circuit.cx(qreg_q[13], qreg_q[5])
circuit.cx(qreg_q[14], qreg_q[6])
circuit.cx(qreg_q[15], qreg_q[7])

#Sbox first half
circuit.cx(qreg_q[2], qreg_q[1])
circuit.x(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[1])
circuit.x(qreg_q[3])
circuit.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.id(qreg_q[0])
circuit.id(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.id(qreg_q[0])
circuit.swap(qreg_q[2], qreg_q[3])
#Sbox second half

circuit.cx(qreg_q[6], qreg_q[5])
circuit.x(qreg_q[4])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.ccx(qreg_q[5], qreg_q[7], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[5])
circuit.x(qreg_q[7])
circuit.ccx(qreg_q[6], qreg_q[4], qreg_q[5])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.swap(qreg_q[6], qreg_q[7])

#Linear
circuit.swap(qreg_q[0], qreg_q[7])
circuit.swap(qreg_q[6], qreg_q[3])
circuit.swap(qreg_q[6], qreg_q[5])
circuit.swap(qreg_q[4], qreg_q[2])
circuit.swap(qreg_q[4], qreg_q[1])

#KEY GEN
circuit.cx(qreg_q[10], qreg_q[9])
circuit.x(qreg_q[8])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[11])
circuit.ccx(qreg_q[9], qreg_q[11], qreg_q[10])
circuit.cx(qreg_q[11], qreg_q[9])
circuit.x(qreg_q[11])
circuit.ccx(qreg_q[10], qreg_q[8], qreg_q[9])
circuit.cx(qreg_q[8], qreg_q[10])
circuit.cx(qreg_q[11], qreg_q[8])
circuit.cx(qreg_q[9], qreg_q[10])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[11])
circuit.swap(qreg_q[10], qreg_q[11])
#Linear
circuit.swap(qreg_q[8], qreg_q[11])
circuit.swap(qreg_q[10], qreg_q[11])
circuit.swap(qreg_q[11], qreg_q[9])

#Sbox 2
circuit.cx(qreg_q[14], qreg_q[13])
circuit.x(qreg_q[12])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.ccx(qreg_q[13], qreg_q[15], qreg_q[14])
circuit.cx(qreg_q[15], qreg_q[13])
circuit.x(qreg_q[15])
circuit.ccx(qreg_q[14], qreg_q[12], qreg_q[13])
circuit.cx(qreg_q[12], qreg_q[14])
circuit.cx(qreg_q[15], qreg_q[12])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.swap(qreg_q[14], qreg_q[15])
#Linear
circuit.swap(qreg_q[12], qreg_q[15])
circuit.swap(qreg_q[14], qreg_q[15])
circuit.swap(qreg_q[15], qreg_q[13])



#2nd round
# Add roundkey
circuit.cx(qreg_q[8], qreg_q[0])
circuit.cx(qreg_q[9], qreg_q[1])
circuit.cx(qreg_q[10], qreg_q[2])
circuit.cx(qreg_q[11], qreg_q[3])
circuit.cx(qreg_q[12], qreg_q[4])
circuit.cx(qreg_q[13], qreg_q[5])
circuit.cx(qreg_q[14], qreg_q[6])
circuit.cx(qreg_q[15], qreg_q[7])
#Sbox first half
circuit.cx(qreg_q[2], qreg_q[1])
circuit.x(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[1])
circuit.x(qreg_q[3])
circuit.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.id(qreg_q[0])
circuit.id(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.id(qreg_q[0])
circuit.swap(qreg_q[2], qreg_q[3])
#Sbox second half

circuit.cx(qreg_q[6], qreg_q[5])
circuit.x(qreg_q[4])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.ccx(qreg_q[5], qreg_q[7], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[5])
circuit.x(qreg_q[7])
circuit.ccx(qreg_q[6], qreg_q[4], qreg_q[5])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.swap(qreg_q[6], qreg_q[7])

#Linear
circuit.swap(qreg_q[0], qreg_q[7])
circuit.swap(qreg_q[6], qreg_q[3])
circuit.swap(qreg_q[6], qreg_q[5])
circuit.swap(qreg_q[4], qreg_q[2])
circuit.swap(qreg_q[4], qreg_q[1])
#//Check output q0 -> q7
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
gate = MCXGate(8)
circuit.append(gate, [0,1,2,3,4,5,6,7,16])
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
#End check output
# #Rev 2nd round
#/////////////////// Rev Linear Layer
circuit.swap(qreg_q[4], qreg_q[1])
circuit.swap(qreg_q[4], qreg_q[2])
circuit.swap(qreg_q[6], qreg_q[5])
circuit.swap(qreg_q[6], qreg_q[3])
circuit.swap(qreg_q[0], qreg_q[7])
#//Rev Sbox first half
circuit.swap(qreg_q[2], qreg_q[3])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.x(qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[3], qreg_q[1])
circuit.x(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[1])
#//Rev Sbox second half
circuit.swap(qreg_q[6], qreg_q[7])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[7], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.x(qreg_q[7])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[4], qreg_q[5])
circuit.cx(qreg_q[7], qreg_q[5])
circuit.x(qreg_q[4])
circuit.ccx(qreg_q[5], qreg_q[7], qreg_q[6])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[5])

# Rev Add roundkey
circuit.cx(qreg_q[8], qreg_q[0])
circuit.cx(qreg_q[9], qreg_q[1])
circuit.cx(qreg_q[10], qreg_q[2])
circuit.cx(qreg_q[11], qreg_q[3])
circuit.cx(qreg_q[12], qreg_q[4])
circuit.cx(qreg_q[13], qreg_q[5])
circuit.cx(qreg_q[14], qreg_q[6])
circuit.cx(qreg_q[15], qreg_q[7])
# #Rev 1st round
# #/////////////////// Rev Linear Layer
circuit.swap(qreg_q[4], qreg_q[1])
circuit.swap(qreg_q[4], qreg_q[2])
circuit.swap(qreg_q[6], qreg_q[5])
circuit.swap(qreg_q[6], qreg_q[3])
circuit.swap(qreg_q[0], qreg_q[7])
#//Rev Sbox first half
circuit.swap(qreg_q[2], qreg_q[3])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.x(qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[3], qreg_q[1])
circuit.x(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[1])
#//Rev Sbox second half
circuit.swap(qreg_q[6], qreg_q[7])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[7], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.x(qreg_q[7])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[4], qreg_q[5])
circuit.cx(qreg_q[7], qreg_q[5])
circuit.x(qreg_q[4])
circuit.ccx(qreg_q[5], qreg_q[7], qreg_q[6])
circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[5])
#End RevSbox second half

#Rev Key Gen
#Linear
circuit.swap(qreg_q[11], qreg_q[9])
circuit.swap(qreg_q[10], qreg_q[11])
circuit.swap(qreg_q[8], qreg_q[11])
#Rev Sbox
circuit.swap(qreg_q[10], qreg_q[11])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[11])
circuit.cx(qreg_q[9], qreg_q[10])
circuit.cx(qreg_q[11], qreg_q[8])
circuit.cx(qreg_q[8], qreg_q[10])
circuit.ccx(qreg_q[10], qreg_q[8], qreg_q[9])
circuit.x(qreg_q[11])
circuit.cx(qreg_q[11], qreg_q[9])
circuit.ccx(qreg_q[9], qreg_q[11], qreg_q[10])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[11])
circuit.x(qreg_q[8])
circuit.cx(qreg_q[10], qreg_q[9])
#Linear
circuit.swap(qreg_q[15], qreg_q[13])
circuit.swap(qreg_q[14], qreg_q[15])
circuit.swap(qreg_q[12], qreg_q[15])

#Sbox 2
circuit.swap(qreg_q[14], qreg_q[15])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.cx(qreg_q[13], qreg_q[14])
circuit.cx(qreg_q[15], qreg_q[12])
circuit.cx(qreg_q[12], qreg_q[14])
circuit.ccx(qreg_q[14], qreg_q[12], qreg_q[13])
circuit.x(qreg_q[15])
circuit.cx(qreg_q[15], qreg_q[13])
circuit.ccx(qreg_q[13], qreg_q[15], qreg_q[14])
circuit.ccx(qreg_q[13], qreg_q[14], qreg_q[15])
circuit.x(qreg_q[12])
circuit.cx(qreg_q[14], qreg_q[13])
##End rev keygen

# Rev Add roundkey
circuit.cx(qreg_q[8], qreg_q[0])
circuit.cx(qreg_q[9], qreg_q[1])
circuit.cx(qreg_q[10], qreg_q[2])
circuit.cx(qreg_q[11], qreg_q[3])
circuit.cx(qreg_q[12], qreg_q[4])
circuit.cx(qreg_q[13], qreg_q[5])
circuit.cx(qreg_q[14], qreg_q[6])
circuit.cx(qreg_q[15], qreg_q[7])
#End Rev Add roundkey
#Grover Diffusion
#//////////////
circuit.h(qreg_q[12])
circuit.h(qreg_q[13])
circuit.h(qreg_q[14])
circuit.h(qreg_q[15])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[10])
circuit.h(qreg_q[11])

circuit.x(qreg_q[12])
circuit.x(qreg_q[13])
circuit.x(qreg_q[14])
circuit.x(qreg_q[15])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])
circuit.x(qreg_q[10])
circuit.x(qreg_q[11])

circuit.h(qreg_q[15])
gate = MCXGate(7)
circuit.append(gate, [8,9,10,11,12,13,14,15])
circuit.h(qreg_q[15])
circuit.x(qreg_q[12])
circuit.x(qreg_q[13])
circuit.x(qreg_q[14])
circuit.x(qreg_q[15])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])
circuit.x(qreg_q[10])
circuit.x(qreg_q[11])
circuit.h(qreg_q[12])
circuit.h(qreg_q[13])
circuit.h(qreg_q[14])
circuit.h(qreg_q[15])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[10])
circuit.h(qreg_q[11])

#Measurement
# circuit.h(qreg_a[0])
circuit.measure(qreg_q[8], creg_c0[0])
circuit.measure(qreg_q[9], creg_c0[1])
circuit.measure(qreg_q[10], creg_c0[2])
circuit.measure(qreg_q[11], creg_c0[3])
circuit.measure(qreg_q[12], creg_c0[4])
circuit.measure(qreg_q[13], creg_c0[5])
circuit.measure(qreg_q[14], creg_c0[6])
circuit.measure(qreg_q[15], creg_c0[7])
print(dict(circuit.count_ops()))
print(circuit.depth())
aersim = AerSimulator()
# Perform an ideal simulation
result_ideal = aersim.run(circuit, shots = 10000000).result()
counts_ideal = result_ideal.get_counts(0)
#sorting the result
sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: -item[1])) 
#sorted_counts = dict(sorted(counts_ideal.items())) 

print(sorted_counts)

# plot_histogram(sorted_counts, sort = 'value', title='Result').show()
# plt.show()


# # Construct a simulator using a noise model
# # from a real backend.
# provider = QiskitRuntimeService()
# backend = provider.get_backend("ibm_brisbane")
# aersim_backend = AerSimulator.from_backend(backend)

# # Perform noisy simulation
# result_noise = aersim_backend.run(circuit).result()
# counts_noise = result_noise.get_counts(0)
# sorted_counts = dict(sorted(counts_noise.items(), key=lambda item: -item[1])) 

# print('Counts(real backend):', sorted_counts)

# plot_histogram(sorted_counts, sort = 'value', title='Result').show()
# plt.show()
