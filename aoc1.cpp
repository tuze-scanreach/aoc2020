#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <fstream>

using namespace std;

#define TARGET_VALUE 2020

int main()
{
    // Read the text file and store each line as an integer in a vector
    ifstream input_file("/home/tuze/repos/aoc2020/aoc1.txt", ios::in);
    string line;
    vector<int> values;
    while (getline(input_file, line))
    {
       values.push_back(stoi(line));
    }

    // Find two values from the vector that add up to 2020 (returns on first match)
    int value1, value2;
    for (auto it = values.begin(); it != values.end(); ++it)
    {
        int index = distance(values.begin(), it);
        value1 = values[index];
        value2 = TARGET_VALUE - values[index];
        auto val2_iterator = find(it, values.end(), value2);
        if (val2_iterator != values.end())
        {
            cout << "The entries are: " << value1 << " and " << value2 << endl;
            cout << "The answer is: " << value1 * value2 << endl;
            break;
        }
    }

    // Find three values that add up to 2020
    // Sorted list helps
    sort(values.begin(), values.end());
    int value3;
    bool search_complete = false;
    for (auto it = values.begin(); it != values.end(); ++it)
    {
        int index = distance(values.begin(), it);
        value1 = values[index];
        int upper_bound_value = TARGET_VALUE - values[index];
        // Get the iterator for the first value larger than the upper_bound_value
        auto upper = upper_bound(it, values.end(), upper_bound_value);
        for (auto it2 = next(it, 1); it2 != upper; ++it2)
        {
            int index2 = distance(values.begin(), it2);
            value2 = values[index2];
            int value3 = TARGET_VALUE - value2 - value1;
            if (value3 == 0)
            {
                break;
            }
            auto val3_iterator = find(it2, upper + 1, value3);
            if (val3_iterator != upper + 1)
            {
                cout << "The entries are: " << value1 << ", " << value2  << " and " << value3 << endl;
                cout << "The answer is: " << value1 * value2 * value3 << endl;
                search_complete = true;
                break;
            }
        }
        if (search_complete)
        {
            break;
        }
        
    }


}