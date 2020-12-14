#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <fstream>
using namespace std;



int main()
{
    // Read the text file and store each line as an integer in a vector
    ifstream input_file("/home/tuze/repos/aoc2020/aoc13.txt", ios::in);
    string line;
    vector<int> values;
    vector<int> indices;
    getline(input_file, line);
    int earliest_boarding = stoi(line);
    getline(input_file, line);
    string delimiter = ",";
    size_t pos;
    int bus_no_index=0;
    while ((pos = line.find(delimiter)) != string::npos) {
        string bus_id = line.substr(0, pos);
        if (bus_id != "x")
        {
            indices.push_back(bus_no_index);
            values.push_back(stoi(bus_id));
        }
        line.erase(0, pos + delimiter.length());
        bus_no_index++;
    }
       indices.push_back(bus_no_index);
       values.push_back(stoi(line));

    int earliest_bus = 0;
    int shortest_wait_time = INT32_MAX;
    for (auto it=values.begin(); it < values.end(); ++it)
    {
        int next_dep_time = (earliest_boarding / (*it) + 1) * (*it);
        if ((next_dep_time - earliest_boarding) < shortest_wait_time)
        {
            shortest_wait_time = next_dep_time - earliest_boarding;
            earliest_bus = *it;
        }
    }
    cout << shortest_wait_time * earliest_bus << endl;


    // Chinese Remainder theorem: https://www.youtube.com/watch?v=zIFehsBHB8o
    vector<long long int> b;
    vector<long long int> n;
    long long int N=1;
    vector<long long int> x;

    for (auto it=values.begin(); it < values.end(); ++it)
    {
        long long int index = distance(values.begin(), it);
        long long int remainder = ((*it) - indices[index]) % (*it);
        b.push_back(remainder);
        n.push_back(*it);
        N *= *it;
    }

    vector<long long int> Ni;
    long long int result = 0;
    for (auto it=n.begin(); it < n.end(); ++it)
    {
        int index = distance(n.begin(), it);
        Ni.push_back(N/(*it));
        for (int i=1; i<1000000; i++)
        {
            if(((N/(*it)) * i) % (*it) == 1)
            {
                x.push_back(i);
                break;
            }
        }
        result += b[index] * Ni[index] * x[index];
    }
    result = result % N;

    cout << result <<endl;
    

    // Brute force:
    long long int val= values[0] ;
    for (; ; val+=values[0]){
        bool found = true;
        for (auto it=values.begin() + 1; it < values.end(); ++it)
        {
            int index = distance(values.begin(), it);
            if((val + indices[index])  % (*it))
            {
                found=false;
                break;
            }
        }
        if (found)
        {
            break;
        }
    }
    cout<< val << endl;
}