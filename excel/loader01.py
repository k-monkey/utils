#!/usr/bin/python
import sys, getopt
import codecs

def main(argv):
    infile = argv[0]
    outfile = argv[1]
    if not infile:
        raise Exception('please provide a text  file to parse with.')
    
    (column_names, rows) = read_rows(infile, delimiter=",")

    if column_names:
        column_names.append("result")
    else:
        column_names = {"result"}

    ord_2_total_dif = {}
    for row in rows:
        ord_2_total_dif[row.get("orderNo2",None)]=float(row.get("orderTotalDiff"))
    
    tolerance = 1e-8
    for row in rows:
        ord_num = row.get("orderNo1", None)
        result = ""
        if ord_num:
            calculated_diff=float(row.get("mstOrderTotal")) - float(row.get("orderTotalSDP"))
            result = abs(calculated_diff-ord_2_total_dif.get(ord_num, float("inf")))<tolerance
        row["result"]=str(result)

    write2file(outfile, column_names, rows, delimiter=",")

def read_rows(fname, delimiter=","):
    print "Loading src file {0}".format(fname)
    rows = []
    with codecs.open(fname, 'r', encoding="utf-8") as src_file:
        headerline = src_file.readline()
        column_names = map(str.strip, str(headerline).split(","))

	for line in src_file:
            rows.append(dict(zip(column_names, map(str.strip, str(line).split(delimiter)))))

    return (column_names, rows)

def write2file(fname, column_names, rows, delimiter=","):
    with codecs.open(fname, 'w', encoding="utf-8") as out_file:
        out_file.write("{0}\n".format(delimiter.join(column_names)))
	for row in rows:
            line = []
            for header in column_names:
                line.append(row.get(header, ""))
            out_file.write("{0}\n".format(delimiter.join(line)))

'''
run the program with 

python calculator.py input_file output_file
'''
if __name__ == '__main__':
    main(sys.argv[1:])
