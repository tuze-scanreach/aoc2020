#include <iostream>
#include <algorithm>
#include <string>
#include <fstream>
#include <map>

using namespace std;

int validate_number(string value)
{
    try
    {
        int number = stoi(value);
        return number;
    }
    catch (const invalid_argument& ia)
    {
        return -1;
    }
}

bool validate_byr(string value)
{
    int number = validate_number(value);
    return (number >= 1920 && number <=2002);
}

bool validate_iyr(string value)
{
    int number = validate_number(value);
    return (number >= 2010 && number <=2020);
}

bool validate_eyr(string value)
{
    int number = validate_number(value);
    return (number >= 2020 && number <=2030);
}

bool validate_hgt(string value)
{
    int min = 150;
    int max = 193;
    size_t unit_loc = value.find("cm");
    if (unit_loc == string::npos)
    {
        min = 59;
        max = 76;
        unit_loc = value.find("in");
    }
    if (unit_loc != string::npos)
    {
        int number = validate_number(value.substr(0, unit_loc));
        return (number >= min && number <=max);
    }
    else
    {
        return false;
    }

}

bool validate_hcl(string value)
{
    if (value[0] == '#')
    {
        for (size_t i=1; i<7; i++)
        {
            if (value[i] < '0' || (value[i] > '9' && value[i] < 'A') || (value[i] > 'Z' && value[i] < 'a') || value[i] > 'z')
            {
                return false;
            }
        }
        return true;
    }
    else
    {
        return false;
    }
}

bool validate_ecl(string value)
{
    string accepted_values[] = {"amb","blu","brn","gry","grn","hzl","oth"};
    string* nPos = find(accepted_values, accepted_values + sizeof(accepted_values)/sizeof(string), value);
    if (nPos != (accepted_values + sizeof(accepted_values)/sizeof(string)))
    {
        return true;
    }
    return false;
}

bool validate_pid(string value)
{
    if (value.length() == 9)
    {
        int number = validate_number(value);
        return (number >= -1);
    }
    else
    {
        return false;
    }
}

bool validate_cid(string value)
{
    return true;
}

typedef bool (*validate_func_t)(string value);

map<string,validate_func_t> validate_key_value = {{"byr", validate_byr}, {"iyr", validate_iyr}, {"eyr", validate_eyr}, {"hgt", validate_hgt}, {"hcl", validate_hcl}, {"ecl", validate_ecl}, {"pid", validate_pid}, {"cid", validate_cid}};

void reset_map(map<string, bool> &pass_keys_map)
{
    for( auto const& [key, val] : pass_keys_map )
    {
        pass_keys_map[key] = (key == "cid");     
    }
}

bool is_map_all_trues(map<string, bool> &pass_keys_map)
{
    bool all_trues = true;
    for( auto const& [key, val] : pass_keys_map )
    {
        all_trues &= val;
    }
    return all_trues;
}

void update_map_with_info_from_text(map<string, bool> &pass_keys_map, string text_info)
{
    for( auto const& [key, val] : pass_keys_map )
    {
        size_t key_loc = text_info.find(key);
        if (key_loc != string::npos)
        {
            //pass_keys_map[key] = true;
            string str_tmp = text_info.substr(key_loc);
            str_tmp = str_tmp.substr(key.length()+1, str_tmp.length());
            string field_value = str_tmp.substr(0, str_tmp.find(' '));
            pass_keys_map[key] = validate_key_value[key](field_value);
            // if (!pass_keys_map[key])
            // {
            //     cout<<key << " is not valid with value " << field_value << endl;
            // }
        }
    }
}


int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc4.txt", ios::in);
    string line;
    vector<int> values;
    map<string,bool> pass_keys_map = {{"byr", false}, {"iyr", false}, {"eyr", false}, {"hgt", false}, {"hcl", false}, {"ecl", false}, {"pid", false}, {"cid", true}};
    int no_valid_passports = 0;

    while (getline(input_file, line))
    {
        if (line == "")
        {
            if (is_map_all_trues(pass_keys_map))
            {
                no_valid_passports++;
            }
            reset_map(pass_keys_map);
        }
        else
        {
            update_map_with_info_from_text(pass_keys_map, line);
        }
        
    }
    // and one last time
    if (is_map_all_trues(pass_keys_map))
    {
        no_valid_passports++;
    }
    cout << no_valid_passports << endl;
}
