#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>

using namespace std;

int main()
{
    int str2[] = {0x01, 0x21, 0x31, 0x7d, 0x1d, 0x5d, 0x07, 0x01, 0x63, 0x6e, 0x35, 0x5f, 0x4b, 0x23, 0x7e};

    string fl = "";

    int v2 = 0x40;
    for (int i = 0; i <= 14; i++)
    {
        int v7 = v2 ^ str2[i];
        v2 = str2[i];
        fl += (char)v7;
        cout << fl << endl;
    }
    cout << fl << endl;
    cout << char(v2 ^ str2[0]) << endl;
}