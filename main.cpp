
#include <iostream>
using namespace std;

int main() {
    int roads[4][4] = {
        {0, 4, 2, 0},
        {4, 0, 0, 5},
        {2, 0, 0, 3},
        {0, 5, 3, 0}
    };

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            cout << roads[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}
