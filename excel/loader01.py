#!/usr/bin/python
import sys, getopt
import codecs
import csv
import copy

def main(argv):
    infile = argv[0]
    outfile = argv[1]
    if not infile:
        raise Exception('please provide a text  file to parse with.')
    
    with codecs.open(infile, 'r', encoding="utf-8") as src_file:
        stylesheet = csv.DictReader(src_file)
        column_names = copy.deepcopy(stylesheet.fieldnames)
        rows=[]
        for row in stylesheet:
            rows.append(row)

    (new_column_names, new_rows) = process(column_names, rows)
    
    with codecs.open(outfile, 'w', encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=new_column_names)
        writer.writeheader()
        map(writer.writerow, new_rows)

def process(column_names, rows):
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
    return (column_names, rows)

'''
run the program with 

python calculator.py input_file output_file
'''
if __name__ == '__main__':
    main(sys.argv[1:])
