#include <iostream>
#include <bitset>

using namespace std;
int main()
{
    /// Change Value Here
    bitset<8> PT{"11011011"};
    bitset<8> K1{"00010010"};
    bitset<4> PT_L = (PT >> 4).to_ulong(), PT_R = PT.to_ulong();
    bitset<4> key1, key2;
    bitset<8> K2, ktemp;
    int sbox[16] = {0xc, 5, 6, 0xb, 9, 0, 0xa, 0xd, 3, 0xe, 0xf, 8, 4, 7, 1, 2};
    int temp1, temp2, temp3, temp0, temp4, temp5, temp6, temp7;
    // key gen
    key1 = (K1 >> 4).to_ullong();
    key2 = K1.to_ullong();
    key1 = sbox[key1.to_ulong()];
    key2 = sbox[key2.to_ulong()];
    temp0 = key1[0];
    temp1 = key1[1];
    temp2 = key1[2];
    temp3 = key1[3];
    key1[0] = temp3;
    key1[1] = temp2;
    key1[2] = temp0;
    key1[3] = temp1;
    temp0 = key2[0];
    temp1 = key2[1];
    temp2 = key2[2];
    temp3 = key2[3];
    key2[0] = temp3;
    key2[1] = temp2;
    key2[2] = temp0;
    key2[3] = temp1;
    ktemp = (key1.to_ulong() << 4);
    K2 = (ktemp.to_ulong() ^ key2.to_ulong());
    cout << "Key = " << K1 << endl;
    cout << "Key = " << K2 << endl;

    cout << "Ban ro = " << PT << endl;

    // Round1
    // cout << "PT= " << PT << endl;
    PT ^= K1;
    cout << "PT^K1= " << PT << endl;

    PT_L = (PT >> 4).to_ulong(), PT_R = PT.to_ulong();
    PT = (sbox[PT_L.to_ullong()] << 4) ^ sbox[PT_R.to_ullong()];
    cout << "PT SBox= " << PT << endl;

    temp0 = PT[0];
    temp1 = PT[1];
    temp2 = PT[2];
    temp3 = PT[3];
    temp4 = PT[4];
    temp5 = PT[5];
    temp6 = PT[6];
    temp7 = PT[7];

    PT[0] = temp7;
    PT[1] = temp2;
    PT[2] = temp4;
    PT[3] = temp6;
    PT[4] = temp1;
    PT[5] = temp3;
    PT[6] = temp5;
    PT[7] = temp0;
    cout << "PT Permu= " << PT << endl;

    // Round2
    // cout << "PT= " << PT << endl;
    PT ^= K2;
    cout << "PT^K2= " << PT << endl;

    PT_L = (PT >> 4).to_ulong(), PT_R = PT.to_ulong();
    PT = (sbox[PT_L.to_ullong()] << 4) ^ sbox[PT_R.to_ullong()];
    cout << "PT SBox= " << PT << endl;

    temp0 = PT[0];
    temp1 = PT[1];
    temp2 = PT[2];
    temp3 = PT[3];
    temp4 = PT[4];
    temp5 = PT[5];
    temp6 = PT[6];
    temp7 = PT[7];

    PT[0] = temp7;
    PT[1] = temp2;
    PT[2] = temp4;
    PT[3] = temp6;
    PT[4] = temp1;
    PT[5] = temp3;
    PT[6] = temp5;
    PT[7] = temp0;
    cout << "PT Permu= " << PT << endl;

    cout << "Ban ma = " << PT << endl;
}