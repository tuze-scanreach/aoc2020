#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstring>
#include <fstream>

using namespace std;

#define TARGET_VALUE 30000000

unsigned int value_indices[TARGET_VALUE];
unsigned int speak_number(unsigned int prev_num_spoken, unsigned int curr_index)
{
    if (value_indices[prev_num_spoken] == UINT32_MAX)
    {
        return 0;
    }
    return curr_index - value_indices[prev_num_spoken] + 1;
}

int main()
{
    const unsigned int input[] = {0,1,5,10,3,12,19};
    memset(value_indices, UINT32_MAX, sizeof(value_indices));
    for (size_t i = 0; i < sizeof(input) / sizeof(input[0]); i++)
    {
        value_indices[input[i]] = i;
    }

    unsigned int num_spoken =  0;
    unsigned int prev_num_spoken = 0;
    for (int i=sizeof(input) / sizeof(input[0]); i < TARGET_VALUE-1; i++)
    {
        num_spoken = speak_number(prev_num_spoken, i-1);
        value_indices[prev_num_spoken] = i;
        prev_num_spoken = num_spoken;
    }
    cout << num_spoken << endl;
}