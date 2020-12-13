#include <iostream>
#include <map>
#include <algorithm>
#include <string>
#include <fstream>
#include <cassert>

using namespace std;


typedef struct
{
  int east;
  int north;
  int moved_east;
  int moved_north;
  char current_dir;
} destination_t;

void swap_waypoint_targets(destination_t *directions)
{
  int temp = directions->east;
  directions->east = directions->north;
  directions->north = temp;
}

void update_direction(destination_t * directions, bool left, int turn_angle)
{
  char directions_left_to_right[] = {'N', 'E', 'S', 'W'};
  map<char, int> directions_left_to_right_index_map = {{'N',0}, {'E',1}, {'S',2}, {'W',3}};
  int no_turns = turn_angle % 90;
  assert(no_turns == 0);
  assert(turn_angle <= 270);
  int multiplier = 1 + (int) left * -2;
  //int new_direction_index = (directions_left_to_right_index_map[directions->current_dir] + multiplier * (turn_angle/90)) % 4;
  //directions->current_dir = directions_left_to_right[new_direction_index];
  int direction_rotation = (multiplier * (turn_angle/90)) % 4;
  if (abs(direction_rotation) == 2) // both just flipped 180degrees
  {
    directions->east *= -1;
    directions->north *= -1;
  }
  else
  {
    swap_waypoint_targets(directions);
    if (direction_rotation == -1 || direction_rotation == 3) // Nort-Sout -> East-West had a flip in sign
    {
      directions->east *= -1;
    }
    else
    {
      directions->north *= -1;
    }
  }
}


void update_destination_directions(destination_t * directions, string line)
{
  char instruction = line[0];
  int value = stoi(line.substr(1, line.length()));
  switch (line[0])
  {
    case 'N':
    directions->north += value;
    break;
    case 'S':
    directions->north -= value;
    break;
    case 'E':
    directions->east += value;
    break;
    case 'W':
    directions->east -= value;
    break;
    case 'L':
    update_direction(directions, true, value);
    break;
    case 'R':
    update_direction(directions, false, value);
    break;
    case 'F':
      directions->moved_east += directions->east * value;
      directions->moved_north += directions->north * value;

    // if (directions->current_dir == 'N' || directions->current_dir == 'S')
    // {
    //   int multiplier = 1 + (int) (directions->current_dir == 'S') * -2;
    //   directions->north += value * multiplier;
    // }
    // else
    // {
    //   int multiplier = 1 + (int) (directions->current_dir == 'W') * -2;
    //   directions->east += value * multiplier;
    // }
    
    break;
  
  default:
    assert(false);
    break;
  }
}

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc12.txt", ios::in);
    string line;
    destination_t direction_to_dest = {.east=10, .north=1, .moved_east=0, .moved_north=0, .current_dir='E'};
    while (getline(input_file, line))
    {
       update_destination_directions(&direction_to_dest, line);
    }
    
    //cout << abs(direction_to_dest.east) + abs(direction_to_dest.north) << endl;
    cout << abs(direction_to_dest.moved_north) + abs(direction_to_dest.moved_east) << endl;
}