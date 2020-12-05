#include <iostream>
#include <algorithm>
#include <string>
#include <fstream>
#include <cassert>

using namespace std;

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc5.txt", ios::in);
    string line;
    vector<int> existing_seat_ids;
    vector<int> seat_ids;

    for (size_t row = 0; row < 127; row++)
    {
      for (size_t col = 0; col < 7; col++)
      {
         seat_ids.push_back(row * 8 + col);
      }
      
    }
    
    
    int highest_seat_id = 0;

    while (getline(input_file, line))
    {
      int min_row = 0;
      int max_row = 127;
      int min_col = 0;
      int max_col = 7;
      for (int i=0; i < line.length(); i++)
      {
        int row_reduction = (max_row - min_row) / 2 + 1;
        int col_reduction = (max_col - min_col) / 2 + 1;
        switch (line[i])
        {
        case 'F':
          max_row -= row_reduction;
          break;
        case 'B':
          min_row += row_reduction;
          break;
        case 'R':
          min_col += col_reduction; 
          break;
        case 'L':
          max_col -= col_reduction;
          break;
        default:
          assert(false);
          break;
        }
        assert(min_row <= max_row);
        assert(min_col <= max_col);
      }
      assert(min_row == max_row);
      assert(min_col == max_col);
      int seat_id = min_row * 8 + min_col;
      //cout << line << " is: " << min_row << " " << min_col << " "<< seat_id << endl;
      existing_seat_ids.push_back(seat_id);
      seat_ids.erase(remove(seat_ids.begin(), seat_ids.end(), seat_id), seat_ids.end());
      if (seat_id > highest_seat_id){
        highest_seat_id = seat_id;
      }
    }

    for (auto it = seat_ids.begin(); it != seat_ids.end(); ++it)
    {
      if (find(existing_seat_ids.begin(), existing_seat_ids.end(), *it - 1) != existing_seat_ids.end())
      {
        if (find(existing_seat_ids.begin(), existing_seat_ids.end(), *it + 1) != existing_seat_ids.end())
        {
          cout << "My Seat is "<< *it << endl;
          break;
        }
      }
    }
    cout << highest_seat_id << endl;
}
