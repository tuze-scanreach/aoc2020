#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <fstream>

using namespace std;

int find_first_left_seat_index(string seats, int seat_index)
{
    int i = seat_index-1;
    for (; i >= 0; i--)
    {
        if (seats[i] != '.')
        {
            break;
        }
    }
    return i;
}

int find_first_right_seat_index(string seats, int seat_index)
{
    int i = seat_index+1;
    for (; i < seats.size(); i++)
    {
        if (seats[i] != '.')
        {
            break;
        }
    }
    return i;
}

bool is_left_occupied(string seats, int seat_index, int offset)
{
    if ((seat_index - offset) > 0 && seats[seat_index - offset -1] == '#')
    {
        return true;
    }
    return false;
}

bool is_left_a_seat(string seats, int seat_index, int offset)
{
    if ((seat_index - offset) > 0 && seats[seat_index - offset -1] != '.')
    {
        return true;
    }
    return false;
}

bool is_right_occupied(string seats, int seat_index, int offset)
{
    if ((seat_index + offset) < seats.size()-1 && seats[seat_index + offset + 1] == '#')
    {
        return true;
    }
    return false;
}

bool is_right_a_seat(string seats, int seat_index, int offset)
{
    if ((seat_index + offset) < seats.size()-1 && seats[seat_index + offset + 1] != '.')
    {
        return true;
    }
    return false;
}

int get_previous_row(vector<string> &seat_map, int seat_index)
{
    if (seat_index == 0)
    {
        return -1;
    }
    else
    {
        return seat_index - 1;
    }
    
}

int get_next_row(vector<string> &seat_map, int seat_index)
{
    if (seat_index >= seat_map.size() - 1)
    {
        return -1;
    }
    else
    {
        return seat_index + 1;
    }
    
}

int get_seat_status(vector<string> &seat_map, int row_index, int seat_index)
{
    string seats = seat_map[row_index];
    int prev_row = get_previous_row(seat_map, row_index);
    int next_row = get_next_row(seat_map, row_index);
    int no_occupied_neighbours = -1;
    bool seats_above_checked[3] = {false};
    bool seats_below_checked[3] = {false};
    int no_visible_seats_above_checked = 0;
    int no_visible_seats_below_checked = 0;
    if (seats[seat_index] != '.')
    {
        int left_seat_offset = seat_index - find_first_left_seat_index(seats, seat_index) - 1;
        int right_seat_offset = find_first_right_seat_index(seats, seat_index) - seat_index - 1;
        no_occupied_neighbours = (int) is_left_occupied(seats, seat_index, left_seat_offset) + (int) is_right_occupied(seats, seat_index, right_seat_offset);
        while((no_visible_seats_above_checked < 3 && -1 < prev_row) || (no_visible_seats_below_checked < 3 && -1 < next_row))
        {

            // Loop here....
            if (prev_row != -1)
            {
                if (!seats_above_checked[0])
                {
                    if (is_left_a_seat(seat_map[prev_row], seat_index, row_index - prev_row - 1))
                    {
                        seats_above_checked[0] = true;
                        no_visible_seats_above_checked++;
                        no_occupied_neighbours += (int) is_left_occupied(seat_map[prev_row], seat_index, row_index - prev_row - 1);
                    }
                }
                if (!seats_above_checked[1])
                {
                    if (seat_map[prev_row][seat_index] != '.')
                    {
                        seats_above_checked[1] = true;
                        no_visible_seats_above_checked++;
                        no_occupied_neighbours += (int) (seat_map[prev_row][seat_index] == '#');

                    }
                }
                if (!seats_above_checked[2])
                {
                    if (is_right_a_seat(seat_map[prev_row], seat_index, row_index - prev_row - 1))
                    {
                        seats_above_checked[2] = true;
                        no_visible_seats_above_checked++;
                        no_occupied_neighbours += (int) is_right_occupied(seat_map[prev_row], seat_index, row_index - prev_row - 1);
                    }
                }
                prev_row = get_previous_row(seat_map, prev_row);
            }
            if (next_row != -1)
            {
                if (!seats_below_checked[0])
                {
                    if (is_left_a_seat(seat_map[next_row], seat_index, next_row - row_index - 1))
                    {
                        seats_below_checked[0] = true;
                        no_visible_seats_below_checked++;
                        no_occupied_neighbours += (int) is_left_occupied(seat_map[next_row], seat_index, next_row - row_index - 1);
                    }
                }
                if (!seats_below_checked[1])
                {
                    if (seat_map[next_row][seat_index] != '.')
                    {
                        seats_below_checked[1] = true;
                        no_visible_seats_below_checked++;
                        no_occupied_neighbours += (int) (seat_map[next_row][seat_index] == '#');

                    }
                }
                if (!seats_below_checked[2])
                {
                    if (is_right_a_seat(seat_map[next_row], seat_index, next_row - row_index - 1))
                    {
                        seats_below_checked[2] = true;
                        no_visible_seats_below_checked++;
                        no_occupied_neighbours += (int) is_right_occupied(seat_map[next_row], seat_index, next_row - row_index - 1);
                    }
                }
                next_row = get_next_row(seat_map, next_row);
            }
        }
    }
    if (no_occupied_neighbours >= 5){
        return 2; // unwanted
    }
    else if (no_occupied_neighbours == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int main()
{
    // Read the text file and store each line as an integer in a vector
    ifstream input_file("/home/tuze/repos/aoc2020/aoc11.txt", ios::in);
    string line;
    vector<string> map_layout;
    vector<string> new_map_layout;
    while (getline(input_file, line))
    {
       map_layout.push_back(line);
    }

    bool layout_changed = true;
    while(layout_changed)
    {
        for (auto it = map_layout.begin(); it < map_layout.end(); it++)
        {
            cout << *it << endl;
        }
        cout << endl << endl;
        layout_changed = false;
        // Filler pass
        for (auto it = map_layout.begin(); it < map_layout.end(); it++)
        {
            string current_line = *it;
            string prev_line;
            if (it == map_layout.begin())
            {
                prev_line = "";
            }
            else
            {
                prev_line = *(it -1);
            }
            string next_line;
            if (it+1 == map_layout.end())
            {
                next_line = "";
            }
            else
            {
                next_line = *(it + 1);
            }
            for (size_t i=0; i < it->size(); i++)
            {
                if (current_line[i] == 'L' && get_seat_status(map_layout, distance(map_layout.begin(), it), i) == 1)
                {
                    layout_changed = true;
                    current_line[i] = '#';
                }
            }
            new_map_layout.push_back(current_line);
        }

        map_layout = new_map_layout;
        for (auto it = map_layout.begin(); it < map_layout.end(); it++)
        {
            cout << *it << endl;
        }
        cout << endl << endl;
        new_map_layout.clear();

        // Vacate pass
        for (auto it = map_layout.begin(); it < map_layout.end(); it++)
        {
            string current_line = *it;
            string prev_line;
            if (it == map_layout.begin())
            {
                prev_line = "";
            }
            else
            {
                prev_line = *(it -1);
            }
            string next_line;
            if (it+1 == map_layout.end())
            {
                next_line = "";
            }
            else
            {
                next_line = *(it + 1);
            }
            for (size_t i=0; i < it->size(); i++)
            {
                if (current_line[i] == '#' && get_seat_status(map_layout, distance(map_layout.begin(), it), i) == 2)
                {
                    layout_changed = true;
                    current_line[i] = 'L';
                }
            }
            new_map_layout.push_back(current_line);
        }
        map_layout = new_map_layout;
        new_map_layout.clear();

        for (auto it = map_layout.begin(); it < map_layout.end(); it++)
        {
            cout << *it << endl;
        }
        cout << endl << endl;
    }

    int no_seats_taken = 0;
    for (auto it = map_layout.begin(); it < map_layout.end(); it++)
    {
        cout << *it << endl;
        for (size_t i=0; i < it->size(); i++)
        {
            if ((*it)[i] == '#')
            {
                no_seats_taken++;
            }
        }
    }

    cout << no_seats_taken << endl;

}