from collections import OrderedDict

from openpyxl import load_workbook
import pandas as pd

# READING NFA TABLE FROM EXCEL FILE
nfa = pd.read_excel(r'input.xlsx', sheet_name='Sheet1', index_col=0)

# READING NUMBER OF TRANSITIONS STATE AND FINAL STATE FROM EXCEL
info = pd.read_excel(r'input.xlsx', sheet_name='Sheet2')
num_transitions = int(info.at[0,'value'])
num_states = int(info.at[1,'value'])
final = info.at[2,'value']
nfa_final_state = [x for x in final.split()]

# converting nfa to dictionary
nfa_t = nfa.transpose()
nfa_dict = nfa_t.to_dict()
print("NFA table\n", nfa_t)

# initialization
new_states_list = []
dfa = {}
keys_list = list(
    list(nfa_dict.keys())[0])  # contains all the states in nfa plus the states created in dfa are also appended further
path_list = list(nfa_dict[keys_list[0]].keys())  # list of all the paths eg: [a,b] or [0,1]


# converting the excel cells values to list
keys = list(
    list(nfa_dict.keys()))
for x in range(num_states):
    for y in range(num_transitions):
        dd = nfa_t[keys[x]][path_list[y]].split(' ')
        nfa_t[keys[x]][path_list[y]] = dd


# Computing DFA transition table
dfa[keys_list[0]] = {}
for y in range(num_transitions):
    state = "".join(nfa_t[keys_list[0]][path_list[y]])
    dfa[keys_list[0]][path_list[y]] = state
    if state not in keys_list:
        new_states_list.append(state)
        keys_list.append(state)
    if state in keys:
        keys.remove(state)

while len(new_states_list) != 0:
    dfa[new_states_list[0]] = {}
    for _ in range(len(new_states_list[0])):
        for i in range(len(path_list)):
            temp = []
            for j in range(len(new_states_list[0])):
                if new_states_list[0][j] != ' ':
                    temp += nfa_t[new_states_list[0][j]][path_list[i]]
            state = ""
            s = state.join(temp)
            state = "".join(OrderedDict.fromkeys(s))
            sorted_char = sorted(state)
            state = "".join(sorted_char)
            if state not in keys_list:
                new_states_list.append(state)
                keys_list.append(state)
                print("state", state)
            if state in keys:
                keys.remove(state)
            dfa[new_states_list[0]][path_list[i]] = state
            print("new", new_states_list)
            print("keys", keys)
    new_states_list.remove(new_states_list[0])
    if len(new_states_list) == 0:
        if len(keys) != 0:
            new_states_list.append(keys[0])


# converting dfa dict to table
dfa_table = pd.DataFrame(dfa)

dfa_final = dfa_table.transpose()

print("DFA Table:\n")
print("dfa",dfa_final)
# writing output to excel file
dfa_final.to_excel("output.xlsx", sheet_name="Sheet1")
