#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <cstring>
#include <cassert>
#include <fstream>

using namespace std;

#define BIT_MASK_36BITS ((1ul<<36) -1)
#define V2 1
void get_mask(string mask, uint64_t * p_or_mask, uint64_t *p_and_mask)
{
    assert(mask.size() == 36);
    for (size_t i=0; i < mask.size(); i++)
    {
        if (mask[i] == '1')
        {
            *p_or_mask |= 1ul << (mask.size() - i - 1);
        }
        if (mask[i] == '0')
        {
            *p_and_mask &= ~(1ul << (mask.size() - i - 1));
        }
    }
}

void get_address_mask(string mask, uint64_t * p_or_mask, uint64_t *p_fuzzy_mask)
{
    assert(mask.size() == 36);
    for (size_t i=0; i < mask.size(); i++)
    {
        if (mask[i] == '1')
        {
            *p_or_mask |= 1ul << (mask.size() - i - 1);
        }
        if (mask[i] == 'X')
        {
            *p_fuzzy_mask |= 1ul << (mask.size() - i - 1);
        }
    }
}

map<uint64_t,uint64_t> permutations;
void apply_fuzzy_mask(map<uint64_t,uint64_t> &mem_map, uint64_t fuzzy_mask, uint64_t address, uint64_t mask_index, uint64_t value)
{
    permutations[fuzzy_mask] ++;
    //cout << fuzzy_mask << ":" << mask_index << endl;
    uint64_t new_address = address | (1ul << mask_index);
    mem_map[new_address] = value & BIT_MASK_36BITS;
    for (int i=mask_index - 1; i >= 0; i--)
    {
        if (fuzzy_mask & (1ul << i))
        {
            apply_fuzzy_mask(mem_map, fuzzy_mask, new_address, i, value);
            break;
        }
    }
    permutations[fuzzy_mask] ++;
    new_address = address & ~(1ul << mask_index);
    mem_map[new_address] = value & BIT_MASK_36BITS;
    for (int i=mask_index - 1; i >= 0; i--)
    {
        if (fuzzy_mask & (1ul << i))
        {
            apply_fuzzy_mask(mem_map, fuzzy_mask, new_address, i, value);
            break;
        }
    }
}

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc14.txt", ios::in);
    string line;
    map<uint64_t,uint64_t> mem_map;
    uint64_t current_or_mask = 0;
    uint64_t current_fuzzy_mask = 0;
    uint64_t current_and_mask = UINT64_MAX;

    while (getline(input_file, line))
    {
        size_t key_word_start_loc = line.find("mask");
        if (key_word_start_loc != string::npos)
        {
            current_or_mask = 0;
            #if V2
            current_fuzzy_mask = 0;
            get_address_mask(line.substr(strlen("mask = "), line.size()), &current_or_mask, &current_fuzzy_mask);
            #else
            current_and_mask = UINT64_MAX;
            get_mask(line.substr(strlen("mask = "), line.size()), &current_or_mask, &current_and_mask);
            #endif
        }
        else
        {
            uint64_t mem_index = stoi(line.substr(strlen("mem["), line.find("]")));
            key_word_start_loc = line.find("=");
            uint64_t mem_value = stoi(line.substr(key_word_start_loc + 2, line.size()));
            #if V2
            mem_index |= current_or_mask;
            mem_index &= ~current_fuzzy_mask;
            for (int i=35; i >= 0; i--)
            {
                if (current_fuzzy_mask & (1ul << i))
                {
                    permutations[current_fuzzy_mask] = 0;
                    apply_fuzzy_mask(mem_map, current_fuzzy_mask, mem_index, i, mem_value);
                    break;
                }
            }
            #else
            mem_value |= current_or_mask;
            mem_value &= current_and_mask;
            mem_map[mem_index] = mem_value & BIT_MASK_36BITS;
            #endif
        }
    }
    __int128 sum = 0;
    for( auto const& [key, val] : permutations )
    {
       // cout << key << ":" << val << endl;
    }
    for( auto const& [key, val] : mem_map )
    {
        sum += val;
    }
    char buffer[100];
    sprintf (buffer, "%lX%lX", (uint64_t)(sum >> 64), (uint64_t)(sum & UINT64_MAX));
    uint64_t result = ((uint64_t) sum);
    cout << buffer << endl;
    cout << result <<endl;
}