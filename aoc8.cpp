#include <iostream>
#include <string>
#include <set>
#include <fstream>
#include <vector>
#include <map>
#include <cassert>

using namespace std;

typedef enum
{
  NOP,
  ACC,
  JMP
} instruction_set_t;

typedef struct
{
  instruction_set_t instruction;
  int argument;
} assembly_instruciton_t;




map<string,instruction_set_t> text_to_instruction = {{"nop", NOP}, {"acc", ACC}, {"jmp", JMP}};

int run_assembly(unsigned int *pc, int accumulator, assembly_instruciton_t assembly)
{
  switch (assembly.instruction)
  {
  case NOP:
    (*pc)++;
    break;
  case ACC:
    (*pc)++;
    accumulator += assembly.argument;
    break;
  case JMP:
    (*pc) += assembly.argument;
    break;
  default:
    break;
  }
  return accumulator;
}

bool run_until_loop_back_or_completion(vector<assembly_instruciton_t> &assembly, int *accumulator)
{
  *accumulator = 0;
  bool loop_back_found = false;
  int execution_count[assembly.size()] = {0};
  unsigned int pc = 0;
  while(!loop_back_found && pc < assembly.size())
  {
    if(++execution_count[pc] > 1)
    {
      loop_back_found = true;
    }
    else
    {
      *accumulator = run_assembly(&pc, *accumulator, assembly[pc]);
    }
  }
  return loop_back_found;

}

int main()
{
    ifstream input_file("/home/tuze/repos/aoc2020/aoc8.txt", ios::in);
    string line;
    vector<assembly_instruciton_t> assembly;
    vector<unsigned int> index_of_nops;
    vector<unsigned int> index_of_jmps;
    while (getline(input_file, line))
    {
      instruction_set_t ass_inst = text_to_instruction[line.substr(0,3)];
      assembly.push_back(assembly_instruciton_t {.instruction = ass_inst,.argument=stoi(line.substr(4, line.length())) });
      if (ass_inst == NOP)
      {
        index_of_nops.push_back(assembly.size() -1);
      }
      else if (ass_inst == JMP)
      {
        index_of_jmps.push_back(assembly.size() -1);
      }
    }

    int accumulator = 0;
    for (auto it = index_of_nops.begin(); it != index_of_nops.end(); ++it)
    {
      assert(assembly[*it].instruction == NOP);
      assembly[*it].instruction = JMP;
      if (!run_until_loop_back_or_completion(assembly, &accumulator))
      {
        cout << accumulator << endl;
        break;
      }
      else
      {
        assembly[*it].instruction = NOP;
      }
    }

    for (auto it = index_of_jmps.begin(); it != index_of_jmps.end(); ++it)
    {
      assert(assembly[*it].instruction == JMP);
      assembly[*it].instruction = NOP;
      if (!run_until_loop_back_or_completion(assembly, &accumulator))
      {
        cout << accumulator << endl;
        break;
      }
      else
      {
        assembly[*it].instruction = JMP;
      }
    }
    
}

