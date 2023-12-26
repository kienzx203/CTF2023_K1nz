#include <bits/stdc++.h>
using namespace std;
int main()
{
    string a2 = "ISPw";
    string Str = "";
    int v4 = 15;
    int v3 = 4;
    for (i = 0;; ++i)
    {
        result = i;
        if (i >= v4)
            break;
        Str[i] ^= a2[i % v3];
    }
    cout << Str;
}