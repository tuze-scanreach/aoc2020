#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cassert>

using namespace std;


int count_string_occurance(string parent, char occurence_of) {
  int count = 0;

  for (int i = 0; i < parent.size(); i++)
    if (parent[i] == occurence_of) count++;

  return count;
}

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc2.txt", ios::in);
    string line;
    int no_valid_passwords_for_early_policy = 0;
    int no_valid_passwords_for_late_policy = 0;
    while (getline(input_file, line))
    {
        // 1-3 a: abcde
        int min_occurence = stoi(line.substr(0, line.find('-')));
        int start_pos = line.find('-') + 1;
        int max_occurence = stoi(line.substr(start_pos, line.find(' ') - start_pos));
        start_pos = line.find(' ') + 1;
        string key_letter = line.substr(start_pos, line.find(':') - start_pos);
        start_pos = line.find(':') + 2;
        string password = line.substr(start_pos, line.length() - start_pos);

        assert(key_letter.size() == 1);

        int occurence_count =  count_string_occurance(password, key_letter[0]);
        if (occurence_count >= min_occurence && occurence_count <= max_occurence)
        {
            no_valid_passwords_for_early_policy++;
        }

        if (key_letter[0] == password[min_occurence -1])
        {
            if (password.length() >= max_occurence)
            {
                if (password[max_occurence - 1] != key_letter[0])
                {
                    no_valid_passwords_for_late_policy++;
                }
            }
            else
            {
                no_valid_passwords_for_late_policy++;
            }
        }
        else if (password.length() >= max_occurence)
        {
             if (password[max_occurence - 1] == key_letter[0])
            {
                no_valid_passwords_for_late_policy++;
            }
        }

    }
    cout << no_valid_passwords_for_early_policy << " are valid for the first policy"<< endl;
    cout << no_valid_passwords_for_late_policy << " are valid for the first policy"<< endl;
}