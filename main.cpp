#include <vector>
#include <algorithm>
#include <fstream>
#include <iostream>

using namespace std;

int liht_dist(string a, string b) {
    int a_size = a.size();
    int b_size = b.size();

    vector<vector<int>> mat(a_size + 1, vector<int>(b_size + 1));

    for (int i = 0; i <= b_size; i++) {
        mat[0][i] = i;
    }

    for (int i = 1; i <= a_size; i++) {
        mat[i][0] = i;
        for (int j = 1; j <= b_size; j++) {
            int comp_cost = (a[i - 1] == b[j - 1]) ? 0 : 1;
            mat[i][j] = min({mat[i - 1][j] + 1, mat[i][j - 1] + 1, mat[i - 1][j - 1] + comp_cost});
        }
    }

    return mat[a_size][b_size];
}

bool my_comparator(const pair<string, int>& a, const pair<string, int>& b) {
    return a.second < b.second;
}

int main() {
    int n = 1000;
    string target;
    ifstream f1("input.txt");
    f1 >> target;
    f1.close();

    ifstream f2("similar_sequences.txt");
    vector<pair<string, int>> options(n);

    for (int i = 0; i < n; i++) {
        f2 >> options[i].first;
        options[i].second = liht_dist(target, options[i].first);
    }
    f2.close();

    sort(options.begin(), options.end(), my_comparator);

    ofstream f3("output/output.txt");
    for (int i = 0; i < 100; i++) {
        f3 << options[i].first << endl;
    }
    f3.close();
    return 0;
}
