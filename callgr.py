import argparse
import sys
import subprocess
import pipes
import os
import fnmatch
import os
import re
import glob

args = None

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

    return parsed_line_list

def get_table_index_recursively(fn_index, fn_call_string, parse_line_list, side, accumulated_idx, level, max_level):
    r_level = level + 1

    my_fn_side = 0
    if side == 1:
        my_fn_side = 0
    else:
        my_fn_side = 1


    if r_level < max_level:
        print(r_level, max_level,len(fn_index),fn_call_string, fn_index)
        for idx in fn_index:
            my_fn_string = parse_line_list[idx][side]
            my_fn_index = get_function_index(my_fn_string, parse_line_list)

            print(idx,my_fn_string,my_fn_index,len(fn_index))
            if my_fn_index[side]:
                temp_fn_idx = []
                for item in my_fn_index[side]:
                    if item not in accumulated_idx:
                        temp_fn_idx.append(item)

                if temp_fn_idx:
                    accumulated_idx = tmp_idx = get_table_index_recursively(temp_fn_idx, my_fn_string, parse_line_list, side, accumulated_idx, r_level, max_level)
                    accumulated_idx.extend(temp_fn_idx)
                    #if tmp_idx:
                    #    =tmp_idx

    return accumulated_idx

def remove_duplicates(line_list):
    retval = list(set(line_list))
    return retval

def parse_arguments():
    global args

    parser = argparse.ArgumentParser(
              description='Generate a call graph for C/C++ projects')

    parser.add_argument(
        dest='functionnames',
        metavar='functionnames',
        nargs='*')

    parser.add_argument('--verbose',
        dest='verbose',
        action='store_true',
        help='verbose mode')

    parser.add_argument('-v', '--version',
        dest='version',
        action='store_true',
        help='display version information')

    parser.add_argument('-o', '--outfile',
        dest='outfile',
        action='store',
        help='output filename')

    parser.add_argument('--include',
        dest='include',
        action='store',
        help='include only function specified')

    parser.add_argument('--exclude',
        dest='exclude',
        action='store',
        help='exclude all functions but those specified')

    parser.add_argument('-A',
        default='9999999',
        dest='calleedepth',
        action='store',
        help='traverse and display x linkage up the stack')

    parser.add_argument('-B',
        default='9999999',
        dest='calldepth',
        action='store',
        help='traverse and display x linkage down the stack')

    parser.add_argument('-u',
        dest='update',
        action='store_true',
        help='updates the file source_mapping with recent rtl information')

    args = parser.parse_args()

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def main():
    parse_arguments()

    if args.update:
        dot_expand_files = find ('*.expand', '.')
        program_arg = ["perl", "/home/ldouglas/perl5/bin/egypt"]
        program_arg.extend(dot_expand_files)
        pipe = subprocess.Popen(program_arg,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        w_file = open(".source_mapping", "w")

        output, error = pipe.communicate()
        if not error:
            print("updating record")
            w_file.writelines(output)
        else:
            print("Error updating record")

        w_file.close()
        pipe.kill()

    file = open(".source_mapping", "r")
    line_list = get_file_content(file)
    file.close()
    #if(arg.functionnames)
    #    function_list =
    parsed_line_list = split_line_list(line_list)

    if args.functionnames:
        fn_string = args.functionnames[0]
        #print("creating gramp", fn_string, dot_pipe )
        fn_idx = get_function_index(fn_string, parsed_line_list)

        accumulated_idx = []
        # handling call side
        if fn_idx[0]:
            fn = parsed_line_list[fn_idx[0][0]]
            accumulated_idx = list(fn_idx[0])
            tmp_idx = get_table_index_recursively(fn_idx[0], fn_string, parsed_line_list, 0, accumulated_idx, 0, int(args.calldepth))
            if tmp_idx:
                accumulated_idx = list(tmp_idx)

        # handling callee side
        if fn_idx[1]:
            fn = parsed_line_list[fn_idx[1][0]]
            accumulated_idx += fn_idx[1]
            tmp_idx = get_table_index_recursively(fn_idx[1], fn_string, parsed_line_list, 1, accumulated_idx, 0, int(args.calleedepth))
            if tmp_idx:
                accumulated_idx = list(tmp_idx)
        
        dot_arg= ["dot", "-Gsize=8.5,11", "-Grankdir=LR", "-Tps", "-o", "cVizGraph.pdf"]
        dot_pipe = subprocess.Popen(dot_arg,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        dot_pipe.stdin.write (line_list[0])
        for idx in accumulated_idx:
            dot_pipe.stdin.write(parsed_line_list[idx][0] + " -> " + parsed_line_list[idx][1] + " " + parsed_line_list[idx][2])
        dot_pipe.stdin.write("\"" + fn_string + "\"" + " [fillcolor=\"red\", style=dotted, style=filled];")
        dot_pipe.stdin.write(line_list[-1])
        
        print(line_list[0])
        for idx in accumulated_idx:
            print(parsed_line_list[idx][0] + " -> " + parsed_line_list[idx][1] + " " + parsed_line_list[idx][2])
        print (line_list[-1])

    else:
        dot_arg= ["dot", "-Gsize=8.5,11", "-Grankdir=LR", "-Tps", "-o", "cVizGraph.pdf"]
        dot_pipe = subprocess.Popen(dot_arg,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        dot_pipe.stdin.write (line_list[0])
        p_idx = 0
        for line in parsed_line_list:
            dot_pipe.stdin.write(parsed_line_list[p_idx][0] + " -> " + parsed_line_list[p_idx][1] + " " + parsed_line_list[p_idx][2])
            print(parsed_line_list[p_idx][0] + " -> " + parsed_line_list[p_idx][1])
            p_idx +=1
        dot_pipe.stdin.write(line_list[-1])
    
    ret_err = dot_pipe.communicate()

    if ret_err: 
        print(ret_err)
