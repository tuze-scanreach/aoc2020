#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <fstream>

using namespace std;



int main()
{
    // Read the text file and store each line as an integer in a vector
    ifstream input_file("/home/tuze/repos/aoc2020/aoc10.txt", ios::in);
    string line;
    vector<int> values;
    while (getline(input_file, line))
    {
       values.push_back(stoi(line));
    }
    sort(values.begin(), values.end());

    int jolt_diff_count[4] = {0};
    int current_output_jolt = 0;
    for (auto it = values.begin(); it != values.end(); ++it)
    {
        if ((*it) - current_output_jolt <= 3)
        {
            jolt_diff_count[(*it) - current_output_jolt]++;
            current_output_jolt = *it;
        }
        else
        {
            cout << "not all adapters can be connected" << endl;
        }
    }
    // increment for the device adapter
    jolt_diff_count[3]++;

    cout << jolt_diff_count[1] << " * " << jolt_diff_count[3] << " = " << jolt_diff_count[1] * jolt_diff_count[3] << endl;

    int max_jolts = *(values.end() - 1);
    long int jolts_list[max_jolts + 4] = {0};
    jolts_list[max_jolts + 3] = 1;
    for (auto it = values.end() - 1; it >= values.begin(); --it)
    {
        int max_val = (*it) + 3;
        for (int i = (*it) + 1; i <= max_val; i++)
        {
            jolts_list[*it] += jolts_list[i];
        }
    }
    int max_val = 3;
    for (int i = 0 + 1; i <= max_val; i++)
    {
        jolts_list[0] += jolts_list[i];
    }


    cout << "Total distinct adapter arrangements: " <<jolts_list[0] << endl;
}