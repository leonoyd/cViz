
def strip_line(line):
    call_index = line.find(' -> ')
    if call_index == -1:
        return []
    call_string = line[:call_index]
    callee_style_string = line[call_index+4:]

    style_index = callee_style_string.find(' [')
    callee_string = callee_style_string[:style_index]
    style_string = callee_style_string[style_index+1:]

    return [call_string, callee_string, style_string]

def get_function_index(fn, parsed_line_list):
    fn_call_indexes = []
    fn_callee_indexes = []
    line_idx = 0
    for line in parsed_line_list:
        if -1 != line[0].find(fn):
            fn_callee_indexes.append(line_idx)
        if -1 !=  line[1].find(fn):
            fn_call_indexes.append(line_idx)
        line_idx = line_idx + 1
    return [fn_call_indexes, fn_callee_indexes]

def get_file_content(file):

    line_list = []
    for line in file:
        line_list.append(line)

    return line_list

def split_line_list(line_list):
    parsed_line_list = []
    for line in line_list[1:-1]:
        ret_list = strip_line(line)
        if ret_list:
            parsed_line_list.append(ret_list)
            #print(ret_list[0], ret_list[1], ret_list[2])

    return parsed_line_list
count = 0

def get_table_index_recursively(fn_index, fn_call_string, parse_line_list, side, accumulated_idx):
    global count
    #if count ==20:
    #    return []
    #count = count +1
    #print("entering fn")
    for idx in fn_index:
        my_fn_string = parse_line_list[idx][side]
        my_fn_index = get_function_index(my_fn_string, parse_line_list)
        if my_fn_index[side]:
            accumulated_idx += my_fn_index[side]
            #for line in my_fn_index[0]:
                #print(parse_line_list[line], line, my_fn_string)
            #print (my_fn_index)
           # print("recursive enter")
            tmp_idx = get_table_index_recursively(my_fn_index[side], my_fn_string, parse_line_list, side, accumulated_idx)
            #print("recursive exit")
            if tmp_idx:
                accumulated_idx +=tmp_idx
                #print (tmp_idx)
        #print(my_fn_string)
            #print(parsed_line_list[idx][0], parsed_line_list[idx][1])
    #print("returning from fn")
    return accumulated_idx

file = open("source_mapping.txt", "r")
line_list = get_file_content(file)
parsed_line_list = split_line_list(line_list)
fn_string = "int lensREDCtrl232(unsigned int)"
fn_idx = get_function_index(fn_string, parsed_line_list)

accumulated_idx = []
# handling call side
if fn_idx[0]:
    fn = parsed_line_list[fn_idx[0][0]]
    accumulated_idx = fn_idx[0]
    tmp_idx = get_table_index_recursively(fn_idx[0], fn_string, parsed_line_list, 0, accumulated_idx)
    if tmp_idx:
        accumulated_idx += tmp_idx

# handling callee side
if fn_idx[1]:
    fn = parsed_line_list[fn_idx[1][0]]
    accumulated_idx += fn_idx[1]
    tmp_idx = get_table_index_recursively(fn_idx[1], fn_string, parsed_line_list, 1, accumulated_idx)
    if tmp_idx:
        accumulated_idx += tmp_idx


print(line_list[0])
for idx in accumulated_idx:
    print(parsed_line_list[idx][0] + " -> " + parsed_line_list[idx][1] + " " + parsed_line_list[idx][2])
print (line_list[-1])
    #for idx in fn_idx[1]:
#    print(parsed_line_list[idx][0], parsed_line_list[idx][1])

line = '"prvIdleTask" -> "xTaskResumeAll" [style=dotted];'
ret_list = strip_line(line)
#while 1:
#    pass
