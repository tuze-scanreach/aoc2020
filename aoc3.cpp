#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cassert>

using namespace std;

typedef struct
{
    int slope_down;
    int slope_right;
} slope_info_t;

slope_info_t possible_slopes[] = {
    {1, 3},
    {1, 1},
    {1, 5},
    {1, 7},
    {2, 1}
};

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc3.txt", ios::in);
    string line;
    vector<int> values;


    for (size_t i = 0; i < sizeof(possible_slopes)/sizeof(slope_info_t); i++)
    {
        int current_loc = 0;
        int trees_encountered = 0;
        int vertical_slope_no = 0;
        while (getline(input_file, line))
        {
            if ((vertical_slope_no % possible_slopes[i].slope_down) > 0)
            {
                vertical_slope_no += 1;
                continue;
            }

            vertical_slope_no += 1;
            if (line[current_loc] == '#')
            {
                trees_encountered += 1;
            }
            current_loc = (current_loc + possible_slopes[i].slope_right) % line.length();
        }
        input_file.clear();
        input_file.seekg(0);
        values.push_back(trees_encountered);
        cout << trees_encountered<< endl;
    }
    uint64_t result = 1;
    for (int i = 0; i < values.size(); i++)
    {
        result *= (values[i]);
    }

    cout << "Result is " << result << endl;
}
