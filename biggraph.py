import ROOT
import time
import csv

outputfile = ROOT.TFile("big_graph.root", "recreate")

h_significance = ROOT.TH2F("my graph", "my graph", 5, 1000, 2000, 10, 0, 1800)

with open('best_significance.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
#        print(row)
#        print(" ")
#        print(row[2])
#        print(type(row[2]))
        h_significance.Fill(x=float(row[0]), y=float(row[1]), w=float(row[2]))
        
outputfile.Write()
outputfile.Close()


