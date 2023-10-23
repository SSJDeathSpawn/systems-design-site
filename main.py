from __future__ import annotations
from typing import List
from flask import Flask, render_template, request

import re

from utils import extract, get_eqns, extract_in_order

app = Flask(__name__)


class Error:
    pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/task_change", methods=['GET', 'POST'])
def task_change():
    error = None
    code = None
    form = dict.fromkeys(['regno', 'type'], "")
    if request.method == "GET":
        return render_template(f"{request.args.get('task')}.html", form=form)
    elif request.method == "POST":
        form = dict(request.form)
        error = [val_task1,
                 val_task2,
                 val_task3,
                 val_task4,
                 val_task5][int(request.args.get('task')[-1])-1]()
        if error is None:
            code = [task1,
                    task2,
                    task3,
                    task4,
                    task5][int(request.args.get('task')[-1])-1]()

    return render_template(f"{request.args.get('task')}.html", error=error, code=code, form=form)


def val_task2():
    pass


def val_task3():
    error = None
    if not bool(re.match(r"\d{2}[A-Z]{3}\d{4}", request.form['regno'])):
        error = Error()
        error.regno = "Invalid registration number"
    return error


def val_task4():
    pass


def val_task5():
    pass


def val_task1():
    error = None
    if not bool(re.match(r"\d{2}[A-Z]{3}\d{4}", request.form['regno'])):
        error = Error()
        error.regno = "Invalid registration number"
    return error


def task1():
    f_vals: List[int] = extract(request.form['regno'])
    beg = '''module task1(a,b,c,d,O);
\tinput a,b,c,d;
\toutput O;
\twire nota, notb, notc, notd;
\tnot not1(nota, a);
\tnot not2(notb, b);
\tnot not3(notc, c);
\tnot not4(notd, d);
'''
    end = 'endmodule'
    tb = '''

module task1_tb;
    reg a,b,c,d;
    wire O;
    task1 inst(a,b,c,d,O);
    integer i;

    initial begin
        for(i=0;i<16;i=i+1) begin
            {a,b,c,d} = i;
            #10;
        end
    end
endmodule'''
    match(request.form['type']):
        case 'AOI':
            eqns = get_eqns(f_vals)
            # Use var count to determine if we even need ands or ors
            var_count = [sum(['A' <= ch <= 'Z' for ch in term]) for term in eqns]
            and_wire_count = [len(list(filter(lambda x: x.isalpha(), i)))-1 for i in eqns]
            or_wire_count = len(eqns)-2
            wires = "\twire "
            for index, count in enumerate(and_wire_count):
                wires += ", ".join([f"andres{index}_{i}" for i in range(count)]) + ", "
            wires += ", ".join([f"orres{i}" for i in range(or_wire_count)])
            wires += ";\n\n"
            ands = ""
            and_count = 0
            for num, term in enumerate(eqns):
                cur = 0
                curNot = False
                first = ""
                second = ""
                for char in term:
                    if cur == 0:
                        if char == "~":
                            curNot = True
                        elif not first:
                            first = ("not" if curNot else "") + char.lower()
                            curNot = False
                        else:
                            second = ("not" if curNot else "") + char.lower()
                            curNot = False
                    else:
                        first = f"andres{num}_{cur-1}"
                        if char == "~":
                            curNot = True
                        else:
                            second = ("not" if curNot else "") + char.lower()

                    if first and second:
                        and_count += 1
                        output = f"andres{num}_{cur}"
                        device = f"and{and_count}"
                        ands += f"\tand {device}({output}, {first}, {second});\n"
                        first = ""
                        second = ""
                        cur += 1
            ands += "\n"
            ors = ""
            for num in range(1, len(eqns)):
                if num == 1:
                    if and_wire_count[num-1] > 0:
                        first = f"andres{num-1}_{and_wire_count[num-1]-1}"
                    else:
                        isNot = "not" if '~' in eqns[num-1] else ""
                        first = isNot + eqns[num-1][-1]
                else:
                    first = f"orres{num-2}"
                second = f"andres{num}_{and_wire_count[num]-1}"
                output = f"orres{num-1}" if num != len(eqns)-1 else "O"

                ors += f"\tor or{num}({output}, {first}, {second});\n"
            mid = wires + ands + ors

            return beg + mid + end + tb

        case 'OAI':
            eqns = get_eqns(f_vals, inverted=True, pos=True)
            or_wire_count = [len(list(filter(lambda x: x.isalpha(), i)))-1 for i in eqns]
            and_wire_count = len(eqns)-2
            wires = "\twire "
            for index, count in enumerate(or_wire_count):
                wires += ", ".join([f"orres{index}_{i}" for i in range(count)]) + ", "
            wires += ", ".join([f"andres{i}" for i in range(and_wire_count)])
            wires += ";\n\n"

            ors = ""
            or_count = 0
            for num, term in enumerate(eqns):
                cur = 0
                curNot = False
                first = ""
                second = ""
                for char in term:
                    if cur == 0:
                        if char == "~":
                            curNot = True
                        elif not first:
                            first = ("not" if curNot else "") + char.lower()
                            curNot = False
                        else:
                            second = ("not" if curNot else "") + char.lower()
                            curNot = False
                    else:
                        first = f"orres{num}_{cur-1}"
                        if char == "~":
                            curNot = True
                        else:
                            second = ("not" if curNot else "") + char.lower()

                    if first and second:
                        or_count += 1
                        output = f"orres{num}_{cur}"
                        device = f"or{or_count}"
                        ors += f"\tor {device}({output}, {first}, {second});\n"
                        first = ""
                        second = ""
                        cur += 1
            ors += "\n"
            ands = ""
            for num in range(1, len(eqns)):
                if num == 1:
                    if or_wire_count[num-1] > 0:
                        first = f"orres{num-1}_{or_wire_count[num-1]-1}"
                    else:
                        isNot = "not" if '~' in eqns[num-1] else ""
                        first = isNot + eqns[num-1][-1]
                else:
                    first = f"andres{num-2}"
                second = f"orres{num}_{or_wire_count[num]-1}"
                output = f"andres{num-1}" if num != len(eqns)-1 else "O"

                ands += f"\tand and{num}({output}, {first}, {second});\n"

            mid = wires + ors + ands

            return beg + mid + end + tb

        case 'NAND':
            eqns = get_eqns(f_vals)
            var_count = [sum(['A' <= ch <= 'Z' for ch in term]) for term in eqns]
            print(var_count)
            and_wire_count = [len(list(filter(lambda x: x.isalpha(), i)))-1 for i in eqns]
            or_wire_count = len(eqns)-2
            wires = "\twire "
            for index, count in enumerate(and_wire_count):
                wires += ", ".join([f"nandres{index}_{i}" for i in range(count)]) + ", "
                wires += ", ".join([f"andres{index}_{i}" for i in range(count-1)]) + ", "
            wires += ", ".join([f"orres{i}" for i in range(or_wire_count)]) + ", "
            wires += ", ".join([f"notorres{i}" for i in range(or_wire_count-1)])
            wires += ";\n\n"
            ands = ""
            and_count = 0
            for num, term in enumerate(eqns):
                cur = 0
                curNot = False
                first = ""
                second = ""
                for char in term:
                    if cur == 0:
                        if char == "~":
                            curNot = True
                        elif not first:
                            first = ("not" if curNot else "") + char.lower()
                            curNot = False
                        else:
                            second = ("not" if curNot else "") + char.lower()
                            curNot = False
                    else:
                        first = f"andres{num}_{cur-1}"
                        if char == "~":
                            curNot = True
                        else:
                            second = ("not" if curNot else "") + char.lower()
                        
                    if first and second:
                        and_count += 1
                        ands += f"\tnand nand{and_count}(nandres{num}_{cur}, {first}, {second});\n"
                        if cur < and_wire_count[num]-1:
                            ands += f"\tnot not{4+and_count}(andres{num}_{cur}, nandres{num}_{cur});\n"
                        first = ""
                        second = ""
                        cur += 1
            ands += "\n"
            ors = ""
            cur = 0
            for num in range(1, len(eqns)):
                if cur == 0:
                    ors += f"\tnand nand{and_count+num}(orres{cur}, nandres0_{and_wire_count[0]-1}, nandres1_{and_wire_count[1]-1});\n"
                    ors += f"\tnot not{4+and_count+num}(notorres{cur}, orres{cur});\n"
                elif num == len(eqns)-1:
                    ors += f"\tnand nand{and_count+num}(O, notorres{cur-1}, nandres{num}_{and_wire_count[num]-1});\n"
                else:
                    ors += f"\tnand nand{and_count+num}(orres{cur}, notorres{cur-1}, nandres{num}_{and_wire_count[num]-1});\n"
                    ors += f"\tnot not{4+and_count+num}(notorres{cur}, orres{cur});\n"
                cur += 1
            mid = wires + ands + ors

            return beg + mid + end + tb

        case 'NOR':
            eqns = get_eqns(f_vals, inverted=True, pos=True)
            var_count = [sum(['A' <= ch <= 'Z' for ch in term]) for term in eqns]
            print(var_count)
            or_wire_count = [len(list(filter(lambda x: x.isalpha(), i)))-1 for i in eqns]
            and_wire_count = len(eqns)-2
            wires = "\twire "
            for index, count in enumerate(or_wire_count):
                wires += ", ".join([f"norres{index}_{i}" for i in range(count)]) + ", "
                if count>1:
                    wires += ", ".join([f"orres{index}_{i}" for i in range(count-1)]) + ", "
            wires += ", ".join([f"andres{i}" for i in range(and_wire_count)]) + ", "
            wires += ", ".join([f"notandres{i}" for i in range(and_wire_count-1)])
            wires += ";\n\n"
            ors = ""
            or_count = 0
            for num, term in enumerate(eqns):
                cur = 0
                curNot = False
                first = ""
                second = ""
                for char in term:
                    if cur == 0:
                        if char == "~":
                            curNot = True
                        elif not first:
                            first = ("not" if curNot else "") + char.lower()
                            curNot = False
                        else:
                            second = ("not" if curNot else "") + char.lower()
                            curNot = False
                    else:
                        first = f"orres{num}_{cur-1}"
                        if char == "~":
                            curNot = True
                        else:
                            second = ("not" if curNot else "") + char.lower()
                        
                    if first and second:
                        or_count += 1
                        ors += f"\tnor nor{or_count}(norres{num}_{cur}, {first}, {second});\n"
                        if cur < or_wire_count[num]-1:
                            ors += f"\tnot not{4+or_count}(orres{num}_{cur}, norres{num}_{cur});\n"
                        first = ""
                        second = ""
                        cur += 1
            ors += "\n"
            ands = ""
            cur = 0
            for num in range(1, len(eqns)):
                if cur == 0:
                    ands += f"\tnor nor{or_count+num}(andres{cur}, norres0_{or_wire_count[0]-1}, norres1_{or_wire_count[1]-1});\n"
                    ands += f"\tnot not{4+or_count+num}(notandres{cur}, andres{cur});\n"
                elif num == len(eqns)-1:
                    ands += f"\tnor nor{or_count+num}(O, notandres{cur-1}, norres{num}_{or_wire_count[num]-1});\n"
                else:
                    ands += f"\tnor nor{or_count+num}(andres{cur}, notandres{cur-1}, norres{num}_{or_wire_count[num]-1});\n"
                    ands += f"\tnot not{4+or_count+num}(notandres{cur}, andres{cur});\n"
                cur += 1
            mid = wires + ors + ands

            return beg + mid + end + tb


def task2():
    pass


def task3():
    f_vals: List[int] = extract(request.form['regno'])
    beg = '''module DEC(O, i);
\tinput[3:0] i;
\toutput[15:0] O;
\tassign O = {i[3] & i[2] & i[1] & i[0], i[3] & i[2] & i[1] & ~i[0], i[3] & i[2] & ~i[1] & i[0], i[3] & i[2] & ~i[1] & ~i[0], i[3] & ~i[2] & i[1] & i[0], i[3] & ~i[2] & i[1] & ~i[0], i[3] & ~i[2] & ~i[1] & i[0], i[3] & ~i[2] & ~i[1] & ~i[0], ~i[3] & i[2] & i[1] & i[0], ~i[3] & i[2] & i[1] & ~i[0], ~i[3] & i[2] & ~i[1] & i[0], ~i[3] & i[2] & ~i[1] & ~i[0], ~i[3] & ~i[2] & i[1] & i[0], ~i[3] & ~i[2] & i[1] & ~i[0], ~i[3] & ~i[2] & ~i[1] & i[0], ~i[3] & ~i[2] & ~i[1] & ~i[0]};
endmodule

module MUX8(O,i,s);
\tinput[7:0] i;
\tinput[2:0] s;
\toutput reg O;
\talways @(i or s) begin
\t\tcase(s)
\t\t\t3'b000:O = i[0];
\t\t\t3'b001:O = i[1];
\t\t\t3'b010:O = i[2];
\t\t\t3'b011:O = i[3];
\t\t\t3'b100:O = i[4];
\t\t\t3'b101:O = i[5];
\t\t\t3'b110:O = i[6];
\t\t\t3'b111:O = i[7];
\t\tendcase
\tend
endmodule

module MUX16(O,i,s);
\tinput[15:0] i;
\tinput[3:0] s;
\toutput reg O;

\talways @(i or s) begin
\t\tcase(s)
\t\t\t4'b0000:O = i[0];
\t\t\t4'b0001:O = i[1];
\t\t\t4'b0010:O = i[2];
\t\t\t4'b0011:O = i[3];
\t\t\t4'b0100:O = i[4];
\t\t\t4'b0101:O = i[5];
\t\t\t4'b0110:O = i[6];
\t\t\t4'b0111:O = i[7];
\t\t\t4'b1000:O = i[8];
\t\t\t4'b1001:O = i[9];
\t\t\t4'b1010:O = i[10];
\t\t\t4'b1011:O = i[11];
\t\t\t4'b1100:O = i[12];
\t\t\t4'b1101:O = i[13];
\t\t\t4'b1110:O = i[14];
\t\t\t4'b1111:O = i[15];
\t\tendcase
\tend
endmodule

module task3(a,b,c,d,O);
\tinput a,b,c,d;
\toutput O;
\twire nota, notb, notc, notd;
\tnot not1(nota, a);
\tnot not2(notb, b);
\tnot not3(notc, c);
\tnot not4(notd, d);
'''
    end = 'endmodule'
    tb = '''

module task3_tb;
\treg a,b,c,d;
\twire O;
\ttask3 inst(a,b,c,d,O);
\tinteger i;

\tinitial begin
\t\tfor(i=0;i<16;i=i+1) begin
\t\t\t{a,b,c,d} = i;
\t\t\t#10;
\t\tend
\tend
endmodule'''

    states = [lambda x: "1'b0",
              lambda x: "not" + x,
              lambda x: x,
              lambda x: "1'b1"]
    match(request.form['type']):

        case "MUX16":
            conns = [states[int(i in f_vals)*3](None) for i in range(15, -1, -1)]

            mid = "\tMUX16 mux(O, "
            mid += f"{{{', '.join(conns)}}}, {{a, b, c, d}});\n"

        case "MUX8A":
            def get_index(n):
                return int(n in f_vals) + int(n+8 in f_vals)*2

            indices = [get_index(i) for i in range(7, -1, -1)]
            conns = [states[index]('a') for index in indices]
            mid = "\tMUX8 mux(O, "
            mid += f"{{{', '.join(conns)}}}, {{b, c, d}});\n"

        case "MUX8B":
            def chunk(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            def get_index(n):
                return int(n in f_vals) + int(n+4 in f_vals)*2

            check_list = sum(list(chunk(list(range(15, -1, -1)), 4))[1::2], [])
            indices = [get_index(i) for i in check_list]
            print(check_list)
            conns = [states[index]('b') for index in indices]
            mid = "\tMUX8 mux(O, "
            mid += f"{{{', '.join(conns)}}}, {{a, c, d}});\n"

        case "MUX8C":
            def chunk(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            def get_index(n):
                return int(n in f_vals) + int(n+2 in f_vals)*2

            check_list = sum(list(chunk(list(range(15, -1, -1)), 2))[1::2], [])
            indices = [get_index(i) for i in check_list]
            print(check_list)
            conns = [states[index]('c') for index in indices]
            mid = "\tMUX8 mux(O, "
            mid += f"{{{', '.join(conns)}}}, {{a, b, d}});\n"

        case "MUX8D":
            def get_index(n):
                return int(n in f_vals) + int(n+1 in f_vals)*2

            indices = [get_index(i) for i in range(14, -1, -2)]
            conns = [states[index]('d') for index in indices]
            mid = "\tMUX8 mux(O, "
            mid += f"{{{', '.join(conns)}}}, {{a, b, c}});\n"

        case "DECODER":
            mid = "\twire[15:0] mid;\n"
            mid += "\tDEC dec(mid, {a,b,c,d});\n"
            mid += f"\tor or1(O, {', '.join([f'mid[{i}]' for i in f_vals])});\n"

    return beg + mid + end + tb


def task4():
    pass


def task5():
    f_vals: List[int] = extract_in_order(request.form['regno'])
    beg = '''module task5(clk, O);
\tinput clk;
\toutput reg[3:0] O;
\talways @(posedge clk) begin
\t\tcase(O)
'''
    end = '''\t\tendcase
\tend
endmodule'''
    tb = '''

module task5_tb;
\treg clk;
\twire[3:0] O;
\ttask5 inst(clk, O);
\tinteger i;

\tinitial begin
\t\tclk = 1'b0;
\t\tfor(i=0;i<20;i=i+1) begin
\t\t\tclk = ~clk;
\t\t\t#5;
\t\tend
\tend
endmodule'''

    mid = ""
    for idx, curr in enumerate(f_vals[:-1]):
        next = f_vals[idx+1]
        mid += f"\t\t\t4'b{bin(curr)[2:].rjust(4, '0')}: O = 4'b{bin(next)[2:].rjust(4, '0')};\n"
    mid += f"\t\t\t4'b{bin(f_vals[-1])[2:].rjust(4, '0')}: O = 4'b{bin(f_vals[0])[2:].rjust(4, '0')};\n"
    mid += f"\t\t\tdefault: O = 4'b{bin(f_vals[0])[2:].rjust(4, '0')};\n"

    return beg + mid + end + tb


app.run(debug=True)
