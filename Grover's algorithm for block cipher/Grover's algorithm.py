from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.circuit.library import MCXGate
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import math
def apply_input(circuit, qreg_q, input_bits):
    """Apply input plaintext to q0-q7 (q7 MSB, q0 LSB)"""
    if len(input_bits) != 8 or not all(bit in '01' for bit in input_bits):
        raise ValueError("Input must be an 8-bit binary string")
    for i, bit in enumerate(reversed(input_bits)):
        if bit == '1':
            circuit.x(qreg_q[i])

def apply_key(circuit, qreg_q, key_bits):
    """Apply key to q8-q15 (q15 MSB, q8 LSB)"""
    if len(key_bits) != 8 or not all(bit in '01' for bit in key_bits):
        raise ValueError("Key must be an 8-bit binary string")
    for i, bit in enumerate(reversed(key_bits)):
        if bit == '1':
            circuit.x(qreg_q[i + 8])

def apply_superposition(circuit, qreg_q, qreg_a):
    """Apply superposition and phase kickback to q8-q15 and ancilla"""
    circuit.x(qreg_a[0])
    for i in range(8, 16):
        circuit.h(qreg_q[i])
    circuit.h(qreg_a[0])

def sbox_first_half(circuit, qreg_q):
    """Apply S-box to q0-q3"""
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
    circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
    circuit.swap(qreg_q[2], qreg_q[3])

def sbox_second_half(circuit, qreg_q):
    """Apply S-box to q4-q7"""
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

def linear_layer(circuit, qreg_q):
    """Apply linear layer to q0-q7"""
    circuit.swap(qreg_q[0], qreg_q[7])
    circuit.swap(qreg_q[6], qreg_q[3])
    circuit.swap(qreg_q[6], qreg_q[5])
    circuit.swap(qreg_q[4], qreg_q[2])
    circuit.swap(qreg_q[4], qreg_q[1])

def add_roundkey(circuit, qreg_q):
    """Add round key (q8-q15) to state (q0-q7)"""
    for i in range(8):
        circuit.cx(qreg_q[i + 8], qreg_q[i])

def key_gen_sbox(circuit, qreg_q, start_idx):
    """Apply S-box for key generation on q[start_idx:start_idx+4]"""
    circuit.cx(qreg_q[start_idx + 2], qreg_q[start_idx + 1])
    circuit.x(qreg_q[start_idx])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 3], qreg_q[start_idx + 2])
    circuit.cx(qreg_q[start_idx + 3], qreg_q[start_idx + 1])
    circuit.x(qreg_q[start_idx + 3])
    circuit.ccx(qreg_q[start_idx + 2], qreg_q[start_idx], qreg_q[start_idx + 1])
    circuit.cx(qreg_q[start_idx], qreg_q[start_idx + 2])
    circuit.cx(qreg_q[start_idx + 3], qreg_q[start_idx])
    circuit.cx(qreg_q[start_idx + 1], qreg_q[start_idx + 2])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.swap(qreg_q[start_idx + 2], qreg_q[start_idx + 3])

def key_gen_linear(circuit, qreg_q, start_idx):
    """Apply linear layer for key generation on q[start_idx:start_idx+4]"""
    circuit.swap(qreg_q[start_idx], qreg_q[start_idx + 3])
    circuit.swap(qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.swap(qreg_q[start_idx + 3], qreg_q[start_idx + 1])

def check_output(circuit, qreg_q, qreg_a, output_bits):
    """Check if q0-q7 matches output_bits (q7 MSB, q0 LSB)"""
    if len(output_bits) != 8 or not all(bit in '01' for bit in output_bits):
        raise ValueError("Output must be an 8-bit binary string")
    for i, bit in enumerate(reversed(output_bits)):
        if bit == '0':
            circuit.x(qreg_q[i])
    gate = MCXGate(8)
    circuit.append(gate, [0, 1, 2, 3, 4, 5, 6, 7, 16])
    for i, bit in enumerate(reversed(output_bits)):
        if bit == '0':
            circuit.x(qreg_q[i])

def rev_sbox_first_half(circuit, qreg_q):
    """Reverse S-box for q0-q3"""
    circuit.swap(qreg_q[2], qreg_q[3])
    circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
    circuit.cx(qreg_q[1], qreg_q[2])
    circuit.cx(qreg_q[3], qreg_q[0])
    circuit.cx(qreg_q[0], qreg_q[2])
    circuit.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
    circuit.x(qreg_q[3])
    circuit.cx(qreg_q[3], qreg_q[1])
    circuit.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
    circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
    circuit.x(qreg_q[0])
    circuit.cx(qreg_q[2], qreg_q[1])

def rev_sbox_second_half(circuit, qreg_q):
    """Reverse S-box for q4-q7"""
    circuit.swap(qreg_q[6], qreg_q[7])
    circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
    circuit.cx(qreg_q[5], qreg_q[6])
    circuit.cx(qreg_q[7], qreg_q[4])
    circuit.cx(qreg_q[4], qreg_q[6])
    circuit.ccx(qreg_q[6], qreg_q[4], qreg_q[5])
    circuit.x(qreg_q[7])
    circuit.cx(qreg_q[7], qreg_q[5])
    circuit.ccx(qreg_q[5], qreg_q[7], qreg_q[6])
    circuit.ccx(qreg_q[5], qreg_q[6], qreg_q[7])
    circuit.x(qreg_q[4])
    circuit.cx(qreg_q[6], qreg_q[5])

def rev_linear_layer(circuit, qreg_q):
    """Reverse linear layer"""
    circuit.swap(qreg_q[4], qreg_q[1])
    circuit.swap(qreg_q[4], qreg_q[2])
    circuit.swap(qreg_q[6], qreg_q[5])
    circuit.swap(qreg_q[6], qreg_q[3])
    circuit.swap(qreg_q[0], qreg_q[7])

def rev_key_gen_sbox(circuit, qreg_q, start_idx):
    """Reverse S-box for key generation"""
    circuit.swap(qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.cx(qreg_q[start_idx + 1], qreg_q[start_idx + 2])
    circuit.cx(qreg_q[start_idx + 3], qreg_q[start_idx])
    circuit.cx(qreg_q[start_idx], qreg_q[start_idx + 2])
    circuit.ccx(qreg_q[start_idx + 2], qreg_q[start_idx], qreg_q[start_idx + 1])
    circuit.x(qreg_q[start_idx + 3])
    circuit.cx(qreg_q[start_idx + 3], qreg_q[start_idx + 1])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 3], qreg_q[start_idx + 2])
    circuit.ccx(qreg_q[start_idx + 1], qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.x(qreg_q[start_idx])
    circuit.cx(qreg_q[start_idx + 2], qreg_q[start_idx + 1])

def grover_diffusion(circuit, qreg_q):
    """Apply Grover diffusion operator on key qubits (q8-q15)"""
    for i in range(8, 16):
        circuit.h(qreg_q[i])
    for i in range(8, 16):
        circuit.x(qreg_q[i])
    circuit.h(qreg_q[15])
    gate = MCXGate(7)
    circuit.append(gate, [8, 9, 10, 11, 12, 13, 14, 15])
    circuit.h(qreg_q[15])
    for i in range(8, 16):
        circuit.x(qreg_q[i])
    for i in range(8, 16):
        circuit.h(qreg_q[i])

def oracle(circuit, qreg_q, qreg_a, output_bits):
    """Apply one iteration of the oracle"""
    # Round 1: Add key, S-box, linear layer
    add_roundkey(circuit, qreg_q)
    sbox_first_half(circuit, qreg_q)
    sbox_second_half(circuit, qreg_q)
    linear_layer(circuit, qreg_q)
    
    # Key schedule: Generate round key
    key_gen_sbox(circuit, qreg_q, 8)
    key_gen_linear(circuit, qreg_q, 8)
    key_gen_sbox(circuit, qreg_q, 12)
    key_gen_linear(circuit, qreg_q, 12)
    
    # Round 2: Add key, S-box, linear layer
    add_roundkey(circuit, qreg_q)
    sbox_first_half(circuit, qreg_q)
    sbox_second_half(circuit, qreg_q)
    linear_layer(circuit, qreg_q)
    
    # Check if output matches expected ciphertext
    check_output(circuit, qreg_q, qreg_a, output_bits)
    
    # Reverse Round 2
    rev_linear_layer(circuit, qreg_q)
    rev_sbox_first_half(circuit, qreg_q)
    rev_sbox_second_half(circuit, qreg_q)
    add_roundkey(circuit, qreg_q)
    
    # Reverse key schedule (in exact reverse order)
    rev_key_gen_linear(circuit, qreg_q, 12)
    rev_key_gen_sbox(circuit, qreg_q, 12)
    rev_key_gen_linear(circuit, qreg_q, 8)
    rev_key_gen_sbox(circuit, qreg_q, 8)
    
    # Reverse Round 1
    rev_linear_layer(circuit, qreg_q)
    rev_sbox_first_half(circuit, qreg_q)
    rev_sbox_second_half(circuit, qreg_q)
    add_roundkey(circuit, qreg_q)

def rev_key_gen_linear(circuit, qreg_q, start_idx):
    """Reverse linear layer for key generation"""
    circuit.swap(qreg_q[start_idx + 3], qreg_q[start_idx + 1])
    circuit.swap(qreg_q[start_idx + 2], qreg_q[start_idx + 3])
    circuit.swap(qreg_q[start_idx], qreg_q[start_idx + 3])

def main(plaintext , ciphertext, r:int):
    # Initialize registers and circuit
    qreg_q = QuantumRegister(16, 'q')
    qreg_a = QuantumRegister(1, 'a')
    creg_c0 = ClassicalRegister(8, 'c0')
    circuit = QuantumCircuit(qreg_q, qreg_a, creg_c0)
    
    # Apply initial operations
    apply_input(circuit, qreg_q, plaintext)
    apply_superposition(circuit, qreg_q, qreg_a)
    
    # Apply oracle and diffusion 12 times
    for _ in range(r):
        oracle(circuit, qreg_q, qreg_a, ciphertext)
        grover_diffusion(circuit, qreg_q)
    
    # Measurement (q8 LSB, q15 MSB)
    for i in range(8):
        circuit.measure(qreg_q[i + 8], creg_c0[i])
    
    # Simulation
    aersim = AerSimulator()
    result_ideal = aersim.run(circuit, shots=100000).result()
    counts_ideal = result_ideal.get_counts(0)
    sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: -item[1]))
    
    # Convert counts to q15 MSB, q8 LSB
    corrected_counts = {}
    for key in sorted_counts:
        corrected_counts[key] = sorted_counts[key]
    
    print("Circuit operations:", dict(circuit.count_ops()))
    print("Circuit depth:", circuit.depth())
    print("Measurement counts (q15 MSB, q8 LSB):", corrected_counts)
    
    plot_histogram(corrected_counts, sort='value', title='Key Distribution (q15 MSB, q8 LSB)')
    plt.show()

if __name__ == "__main__":
    N = 2**8
    M = 1 # number of keys
    plaintext = "11011011"
    ciphertext = "00100010"
    r = int(math.pi/4*math.sqrt(N/M))
    print(r)
    main(plaintext,ciphertext, r)
