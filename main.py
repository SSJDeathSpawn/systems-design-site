from __future__ import annotations
from typing import List
from flask import Flask, render_template, request
import re

from utils import extract, notop, get_eqns

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
    pass


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
                        ands += f"\tand and{and_count}(andres{num}_{cur}, {first}, {second});\n"
                        first = ""
                        second = ""
                        cur += 1
            ands += "\n"
            ors = ""
            cur = 0
            for num in range(1, len(eqns)):
                if cur == 0:
                    ors += f"\tor or{num}(orres{cur}, andres0_{and_wire_count[0]-1}, andres1_{and_wire_count[1]-1});\n"
                elif num == len(eqns)-1:
                    ors += f"\tor or{num}(O, orres{cur-1}, andres{num}_{and_wire_count[num]-1});\n"
                else:
                    ors += f"\tor or{num}(orres{cur}, orres{cur-1}, andres{num}_{and_wire_count[num]-1});\n"
                cur += 1
            mid = wires + ands + ors

            return beg + mid + end + tb

        case 'OAI':
            f_vals = notop(f_vals)
            return "OAI"

        case 'NAND':
            eqns = get_eqns(f_vals)
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
            f_vals = notop(f_vals)
            return "NOR"


def task2():
    pass


def task3():
    pass


def task4():
    pass


def task5():
    pass


app.run(debug=True)
