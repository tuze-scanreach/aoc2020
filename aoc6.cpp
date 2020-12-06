#include <iostream>
#include <string>
#include <set>
#include <fstream>

using namespace std;

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc6.txt", ios::in);
    string line;

    int total_yes_answers = 0;
    int total_unanimous_yes_answers = 0;
    set<char> group_yes_values;
    string overlapping_yes_values = "";
    string prev_line = "";
    while (getline(input_file, line))
    {
      if (line == "")
      {
        total_yes_answers += group_yes_values.size();
        total_unanimous_yes_answers += overlapping_yes_values.length();
        overlapping_yes_values = "";
        group_yes_values.clear();
      }
      else
      {
        if (prev_line == "")
        {
          overlapping_yes_values = line;
        }
        else
        {
          string overlap_with_current_line = "";
          for (size_t i = 0; i < line.length(); i++)
          {
            size_t found = overlapping_yes_values.find(line[i]);
            if (found != string::npos)
            {
              overlap_with_current_line += line[i];
            }
          }
          overlapping_yes_values = overlap_with_current_line;
        }
        
        
        for (size_t i = 0; i < line.length(); i++)
        {
          group_yes_values.insert(line[i]);
        }
      }

      prev_line = line;
    }
    // The last group:
    total_yes_answers += group_yes_values.size();
    total_unanimous_yes_answers += overlapping_yes_values.length();

    cout << total_yes_answers << endl;
    cout << total_unanimous_yes_answers << endl;
}
