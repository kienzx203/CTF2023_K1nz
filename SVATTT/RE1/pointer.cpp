#include <bits/stdc++.h>
using namespace std;
int sthIdontknow(char b, char k)
{
    char b2;
    for (size_t i = 0; i < 8; ++i)
    {
        if (((b >> i) & 1) == ((k >> i) & 1))
            b2 = ((1 << i) ^ -1) & b & 255;
        else
            b2 = ((1 << i) & 255) | b;
        b = (char)b2;
    }
    return b;
}
int main()
{
    char sth[] = "pearldarkk";
    char mySth[] = {0x45, 0xd, 0x50, 0x1c, 0x5d, 0xa, 0x46, 0x2d,
                    0x5e, 0x1f, 0x44, 0x17, 0x54, 0x2d, 0x6, 0x11,
                    0x54, 0x6, 0x34, 0x7, 0x41, 0xe, 0x52, 0x2d,
                    0x19, 0x16, 0x3e, 0x1, 0x6, 0x5a, 0x1c, 0x56};
    string key;
    for (int i = 0; i < 32; i++)
    {
        for (int j = 0; j < 156; j++)
        {
            if (!(sthIdontknow(sth[i % 10], char(j)) ^ char(mySth[i])))
                key.push_back(char(j));
        }
    }
    cout << key << endl;
}