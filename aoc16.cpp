#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <string>
#include <cstring>
#include <cassert>
#include <fstream>

using namespace std;

typedef struct
{
    int rangeStart;
    int rangeEnd;
    string name;
} range_t;


tuple<int, bool> get_error_val(vector<range_t> &valid_ranges, int value)
{
    bool inrange = false;
    for (auto it=valid_ranges.begin(); it < valid_ranges.end(); it++)
    {
        if ((it->rangeStart <= value) && (it->rangeEnd >= value))
        {
            inrange = true;
            break;
        }

    }
    if (!inrange)
    {
        return make_tuple(value,true);
    }
    return make_tuple(0, false);
}

void update_match(vector<range_t> &valid_ranges, vector<vector<string>> &names, int value, int index)
{
    bool inrange = false;
    vector<string> matched_names;
    for (auto it=valid_ranges.begin(); it < valid_ranges.end(); it++)
    {
        if (it->rangeStart <= value && it->rangeEnd >= value)
        {
            matched_names.push_back(it->name);
        }

    }
    assert(matched_names.size() > 0);
    if(names.size() <= index)
    {
        assert(names.size() == index);
        names.push_back(matched_names);
    }
    else
    {
        for (auto it = names[index].begin(); it < names[index].end(); )
        {
            auto found_entry = find(matched_names.begin(), matched_names.end(), *it);
            if (found_entry == matched_names.end())
            {
                // if (index == 10)
                //     cout << index << ": " << *it << endl;
               it =  names[index].erase(it);
            }
            else
            {
                // if (index == 10)
                //     cout << index << ": " << *it << endl;
                it++;
            }
            
        }
        
    }
}


void prune_matched_names(vector<vector<string>> &names, map<string, int> &name_map)
{
    bool updates_done = false;
    bool prune_complete = true;
    do
    {
        updates_done = false;
        prune_complete = true;
        for (auto names_it = names.begin(); names_it<names.end();names_it++)
        {
            bool only_one = false;
            vector<string> matched_names;
            if(names_it->size() == 1)
            {
                only_one = true;
                auto it = names_it->begin();
                name_map[*it] = distance(names.begin(), names_it);
            }
            auto only_entry_it = names_it->end();
            for (auto it = names_it->begin(); it < names_it->end(); ++it )
            {
                only_entry_it = it;
                for (auto names_it2 = names.begin(); names_it2<names.end();names_it2++)
                {
                    if((names_it == names_it2) || names_it2->size() == 1)
                    {
                        continue;
                    }
                    else if (only_one)
                    {
                        prune_complete = false;
                        updates_done = true;
                        only_entry_it = names_it->end();
                        names_it2->erase(remove(names_it2->begin(), names_it2->end(), *it), names_it2->end());
                    }
                    else
                    {
                        prune_complete = false;
                        auto found_entry = find(names_it2->begin(), names_it2->end(), *it);
                        if (found_entry != names_it2->end())
                        {
                            only_entry_it = names_it->end();
                        }
                    }
                }
                if (only_entry_it != names_it->end())
                {
                    name_map[*only_entry_it] = distance(names.begin(), names_it);
                    break;
                }
            }
            if (only_entry_it != names_it->end())
            {
                string entry = *only_entry_it;
                names_it->clear();
                names_it->push_back(entry);
                updates_done = true;
            }
        }
    } while(updates_done && !prune_complete);
}




int main()
{
    vector<range_t> valid_ranges;
    vector<vector<int>> ticket_vals;
    vector<vector<string>> names;
    // Read the text file and store each line as an integer in a vector
    ifstream input_file("/home/tuze/repos/aoc2020/aoc16.txt", ios::in);
    string line;
    vector<string> values;
    bool read_in_ranges = true; 
    bool read_in_tickets = false;
    long unsigned int error_rate = 0;
    while (getline(input_file, line))
    {
        vector<int> vals;
        long unsigned int start_error_rate = error_rate;
        bool bad_ticket = false;
        if (line == "")
        {
            read_in_ranges = false;
            read_in_tickets = false;
            continue;
        }
        else if(read_in_ranges)
        {
            string name = line.substr(0, line.find(':'));
            line = line.substr(line.find(':')+2, line.length());
            int rangeStart = stoi(line.substr(0,line.find('-')));
            line = line.substr(line.find('-')+1, line.length());
            int rangeEnd = stoi(line.substr(0,line.find(' ')));
            valid_ranges.push_back(range_t {.rangeStart = rangeStart, .rangeEnd = rangeEnd, .name = name});
            line = line.substr(line.find(' ')+4, line.length());
            rangeStart = stoi(line.substr(0,line.find('-')));
            line = line.substr(line.find('-')+1, line.length());
            rangeEnd = stoi(line.substr(0,line.find(' ')));
            valid_ranges.push_back(range_t {.rangeStart = rangeStart, .rangeEnd = rangeEnd, .name = name});
        }
        else if (read_in_tickets)
        {
            size_t comma_loc = line.find(",");
            while (comma_loc != string::npos)
            {
                int value = stoi(line.substr(0, comma_loc));
                vals.push_back(value);
                auto err_check = get_error_val(valid_ranges, value);
                bad_ticket |= get<1>(err_check);
                error_rate += get<0>(err_check);
                line = line.substr(comma_loc + 1, line.length());
                comma_loc = line.find(",");
            }
            int value = stoi(line);
            vals.push_back(value);
            auto err_check = get_error_val(valid_ranges, value);
            bad_ticket |= get<1>(err_check);
            error_rate += get<0>(err_check);
            if (!bad_ticket)
            {
                ticket_vals.push_back(vals);
            }
        }
        else
        {
            read_in_tickets = true;
        }
    }

    for (auto vals_it = ticket_vals.begin(); vals_it < ticket_vals.end(); vals_it++)
    {
        for (auto it=vals_it->begin(); it < vals_it->end(); it++)
        {
            int index = distance(vals_it->begin(), it);
            update_match(valid_ranges, names, *it, index);
        }
    }
    map<string, int> name_map;
    prune_matched_names(names, name_map);

    long unsigned int result = 1;
    for (auto const& [key,val]: name_map)
    {
        if (key.find("departure") != string::npos)
        {
            result *= ticket_vals[0][val];
        }
    }
    cout << error_rate << endl;
    cout << result << endl;
}