#include <iostream>
#include <string>
#include <set>
#include <fstream>
#include <map>
#include <vector>
#include <tuple>
#include <cassert>

using namespace std;

typedef struct
{
    vector<string> parent;
    vector<tuple<string, int>> child;
}parent_child_t;

string get_colour_name(string line)
{
    size_t colour_name_end_loc = line.find("bag");
    if (colour_name_end_loc != string::npos)
    {
        string colour_name = line.substr(0, colour_name_end_loc-1);
        return colour_name;
    }
    assert(false);
    return "";
}

int main()
{
    map<string, int> bag_colour_relation_ship_list;
    vector<parent_child_t> storage;

    ifstream input_file("/home/tuze/repos/aoc2020/aoc7.txt", ios::in);
    string line;
    while (getline(input_file, line))
    {
        string colour_name = get_colour_name(line);
        string count_for_current_child = "";
        int storage_index = storage.size();
        if (bag_colour_relation_ship_list.find(colour_name) == bag_colour_relation_ship_list.end())
        {
            bag_colour_relation_ship_list[colour_name] = storage_index;
            parent_child_t *t = new parent_child_t;
            storage.push_back(*t);
        }
        else
        {
            storage_index = bag_colour_relation_ship_list[colour_name];
        }
        
        for (size_t i = 0; i < line.length(); i++)
        {
            if (isdigit(line[i]))
            {
                count_for_current_child += line[i];
            }
            else if (count_for_current_child != "")
            {
                string child_colour_name = get_colour_name(line.substr(i+1, line.length()));
                //cout << child_colour_name << endl;
                //bag_colour_relation_ship_list[colour_name].child.push_back(child_colour_name);
                storage[storage_index].child.push_back(make_tuple(child_colour_name, stoi(count_for_current_child)));
                int child_storage_index = storage.size();
                if (bag_colour_relation_ship_list.find(child_colour_name) == bag_colour_relation_ship_list.end())
                {
                    //cout << child_colour_name << " " << child_storage_index;
                    bag_colour_relation_ship_list[child_colour_name] = child_storage_index;
                    parent_child_t *c = new parent_child_t;
                    storage.push_back(*c);
                    //bag_colour_relation_ship_list[child_colour_name] = storage.back();
                    
                }
                else 
                {
                    child_storage_index = bag_colour_relation_ship_list[child_colour_name];
                }
                
                //bag_colour_relation_ship_list[child_colour_name].parent.push_back(colour_name);
                storage[child_storage_index].parent.push_back(colour_name);
                count_for_current_child = "";
            }
            else if (line[i] == '.')
            {
                break;
            }
        }
    }

    cout << bag_colour_relation_ship_list["shiny gold"] << endl;
    vector<string> parents = storage[bag_colour_relation_ship_list["shiny gold"]].parent;
    set<string> unique_parents;
    while(parents.size() != 0)
    {
        auto parent_it = parents.begin();
        string colour_name = *parent_it;
        
        parents.erase(parent_it);
        unique_parents.insert(colour_name);
        parents.insert(parents.end(), storage[bag_colour_relation_ship_list[colour_name]].parent.begin(), storage[bag_colour_relation_ship_list[colour_name]].parent.end());
        
    }

    cout << unique_parents.size() << endl;

    vector<tuple<string, int>> children = storage[bag_colour_relation_ship_list["shiny gold"]].child;
    int total_bags_required = 0;
    while(children.size() != 0)
    {
        auto child_it = children.begin();
        string colour_name;
        int no_bags;
        tie (colour_name, no_bags) = *child_it;
        total_bags_required += no_bags ;
        children.erase(child_it);
        //cout << colour_name << " " << no_bags <<endl;
        for (size_t i = 0; i < no_bags; i++)
        {
            children.insert(children.end(), storage[bag_colour_relation_ship_list[colour_name]].child.begin(), storage[bag_colour_relation_ship_list[colour_name]].child.end());
        }

    }
    cout<< total_bags_required<<endl;
}

