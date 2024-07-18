#include <iostream>
#include <fstream>
#include <cstdint>
#include <math.h>
using namespace std;
int main()
{
	int n = 4; // number of bit
	int K = 9; // number of GATES
	int N = pow(2, n);
	fstream output("SBoxSolver.py", ios::out);
	// Pi0 = [0xC, 4, 6, 2, 0xA ,5 ,0xB ,0x9 ,0xE ,8, 0xD ,7 ,0 ,3 ,0xF, 1]
	// π1' = (6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15);
	// π2' = (11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0);
	// π3' = (12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11);
	// π4' = (7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12);
	// π5' = (5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0);
	// π6' = (8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7);
	// π7' = (1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2);
	// Magma
	// uint8_t Sbox[N] = {0xC, 4, 6, 2, 0xA, 5, 0xB, 0x9, 0xE, 8, 0xD, 7, 0, 3, 0xF, 1}; // SBOX

	// PRESENT
	uint8_t Sbox[N] = {0xC, 5, 6, 0xB, 0x9, 0, 0xA, 0xD, 3, 0xE, 0xF, 0x8, 4, 7, 1, 2}; // SBOX
	// GIFT
	// uint8_t Sbox[N] = {0x1, 0xa, 4, 0xc, 6, 0xf, 3, 0x9, 2, 0xd, 0xb, 7, 5, 0, 0x8, 0xe}; // SBOX
	// test
	//  uint8_t Sbox[N] = {0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 11, 10, 13, 12, 15, 14};
	//  Keccak
	// uint8_t Sbox[N] = {0, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16, 19, 30, 25, 28, 31};
	uint8_t y[N][n];  // Output
	uint8_t x0[N][n]; // Input
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < n; j++)
		{
			y[i][j] = (Sbox[i] >> (n - 1 - j)) & 0x1;
			x0[i][j] = (i >> (n - 1 - j)) & 0x1;
		}
	}

	output << "from z3 import *\n";
	// x generator
	for (int i = 0; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < n; j++)
			{
				output << "x_" << i << "_" << s << j << ",";
			}
		}
	}
	// y generator
	for (int i = 0; i < N; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "y_" << i << s << ",";
		}
	}
	// q generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < 3; j++)
			{
				output << "q_" << i << "_" << s << j << ",";
			}
		}
	}
	// a generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 2 * n + n; j++)
		{
			output << "a_" << i << j << ",";
		}
	}
	// b generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			output << "b_" << i << j << ",";
		}
	}
	// t generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			output << "t_" << i << "_" << s << ",";
		}
	}
	// m generator
	for (int i = 0; i < n; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "m_" << i << s;
			if ((i != n - 1) || (s != n - 1))
				output << ",";
		}
	}
	output << "= BitVecs('";
	// x generator
	for (int i = 0; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < n; j++)
			{
				output << "x_" << i << "_" << s << j << " ";
			}
		}
	}
	// y generator
	for (int i = 0; i < N; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "y_" << i << s << " ";
		}
	}
	// q generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < 3; j++)
			{
				output << "q_" << i << "_" << s << j << " ";
			}
		}
	}
	// a generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 2 * n + n; j++)
		{
			output << "a_" << i << j << " ";
		}
	}
	// b generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			output << "b_" << i << j << " ";
		}
	}
	// t generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			output << "t_" << i << "_" << s << " ";
		}
	}
	// m generator
	for (int i = 0; i < n; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "m_" << i << s;
			if ((i != n - 1) || (s != n - 1))
				output << " ";
		}
	}
	output << "',3)\n";
	output << "s = Solver()\n";

	// x generator
	for (int i = 0; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < n; j++)
			{
				output << "s.add(x_" << i << "_" << s << j << "<2)\n";
				output << "s.add(x_" << i << "_" << s << j << ">=0)\n";
			}
		}
	}
	// y generator
	for (int i = 0; i < N; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "s.add(y_" << i << s << "<2)\n";
			output << "s.add(y_" << i << s << ">=0)\n";
		}
	}
	// q generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			for (int j = 0; j < 3; j++)
			{
				output << "s.add(q_" << i << "_" << s << j << "<2)\n";
				output << "s.add(q_" << i << "_" << s << j << ">=0)\n";
			}
		}
	}
	// a generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 2 * n + n; j++)
		{
			output << "s.add(a_" << i << j << "<2)\n";
			output << "s.add(a_" << i << j << ">=0)\n";
		}
	}
	// b generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			output << "s.add(b_" << i << j << "<2)\n";
			output << "s.add(b_" << i << j << ">=0)\n";
		}
	}
	// t generator
	for (int i = 1; i < K + 1; i++)
	{
		for (int s = 0; s < N; s++)
		{
			output << "s.add(t_" << i << "_" << s << "<2)\n";
			output << "s.add(t_" << i << "_" << s << ">=0)\n";
		}
	}
	// m generator
	for (int i = 0; i < n; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "s.add(m_" << i << s << "<2)\n";
			output << "s.add(m_" << i << s << ">=0)\n";
		}
	}

	for (int s = 0; s < N; s++)
	{
		for (int i = 0; i < n; i++)
		{
			output << "s.add(x_0_" << s << i << "==" << (int)x0[s][i] << ")\n";
		}
	}
	for (int i = 0; i < N; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "s.add(y_" << i << s << "==" << (int)y[i][s] << ")\n";
		}
	}

	for (int s = 0; s < N; s++)
	{
		for (int k = 1; k < K + 1; k++)
		{
			for (int l = 0; l < 3; l++)
			{
				output << "s.add(q_" << k << "_" << s << l << "==";
				for (int i = 0; i < n; i++)
				{
					output << "(a_" << k << (n * l + i) << "*x_" << (k - 1) << "_" << s << i;
					if (i != n - 1)
						output << ")^";
					else
						output << "))\n";
				}
			}
			output << "s.add(t_" << k << "_" << s << "== q_" << k << "_" << s << 0 << "^b_" << k << 0 << "^(b_" << k << 1 << "*q_" << k << "_" << s << 1 << ")^(b_" << k << 2 << "*q_" << k << "_" << s << 1 << "*" << "q_" << k << "_" << s << 2 << "))\n";
			for (int i = 0; i < n; i++)
			{
				output << "s.add(x_" << k << "_" << s << i << "== (a_" << k << i << "*t_" << k << "_" << s << ")^(1^a_" << k << i << ")*x_" << k - 1 << "_" << s << i << ")\n";
			}
		}
		for (int j = 0; j < n; j++)
		{
			output << "s.add(y_" << s << j << "==";
			for (int i = 0; i < n; i++)
			{
				output << "(m_" << j << i << "*x_" << K << "_" << s << i;
				if (i != n - 1)
					output << ")^";
				else
					output << "))\n";
			}
		}
	}
	// for a
	for (int k = 1; k < K + 1; k++)
	{
		for (int l = 0; l < 3; l++)
		{
			output << "s.add(1==";
			for (int i = 0; i < n; i++)
			{
				output << "a_" << k << (n * l + i);
				if (i != n - 1)
					output << "+";
				else
					output << ")\n";
			}
		}
	}
	// for a
	for (int i = 0; i < n; i++)
	{
		for (int k = 1; k < K + 1; k++)
		{
			output << "s.add(2 > ";
			for (int l = 0; l < 3; l++)
			{
				{
					output << "a_" << k << (n * l) + i;
					if (l != 2)
						output << "+";
					else
						output << ")\n";
				}
			}
		}
	}
	// for b
	for (int k = 1; k < K + 1; k++)
	{
		output << "s.add(1 == ";
		output << "b_" << k << 0 << "+" << "b_" << k << 1 << "+" << "b_" << k << 2 << ")\n";
	}
	// condition for m
	for (int i = 0; i < n; i++)
	{
		output << "s.add(1==";
		for (int s = 0; s < n; s++)
		{
			output << "m_" << i << s;
			if (s != n - 1)
				output << "+";
			else
				output << ")\n";
		}
	}
	for (int i = 0; i < n; i++)
	{
		output << "s.add(1==";
		for (int s = 0; s < n; s++)
		{
			output << "m_" << s << i;
			if (s != n - 1)
				output << "+";
			else
				output << ")\n";
		}
	}

	output << "\nif s.check() == sat:\n\tm = s.model()\n";
	for (int i = 1; i < K + 1; i++)
	{
		output << "\tprint (\"b_" << i << "0 = %s\" % m[b_" << i << "0])\n";
		output << "\tprint (\"b_" << i << "1 = %s\" % m[b_" << i << "1])\n";
		output << "\tprint (\"b_" << i << "2 = %s\" % m[b_" << i << "2])\n";
	}
	for (int i = 1; i < K + 1; i++)
	{
		for (int j = 0; j < 2 * n + n; j++)
		{
			output << "\tif m[a_" << i << j << "]==1 : print(\"a_" << i << j << "= %s\" % m[a_" << i << j << "])\n";
		}
	}
	for (int i = 0; i < n; i++)
	{
		for (int s = 0; s < n; s++)
		{
			output << "\tif m[m_" << i << s << "]==1 : print(\"m_" << i << s << "= %s\" % m[m_" << i << s << "])\n";
		}
	}
	output << "else: print(\"unsat\")";
}