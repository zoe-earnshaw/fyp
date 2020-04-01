import ROOT
import argparse
import csv
#import numpy as np

#defining class to organise histogram attributes
class hist_attributes:
    def __init__(self, name="", title="", start=0, stop=100, step=10):
        print("Creating hist attributes!")
        self.hist_name = name
        self.x_axis_title = title
        self.stop = stop
        self.start = start
        self.step = step
        self.tag = ""

#taking signal point info from input
parser = argparse.ArgumentParser()
parser.add_argument("stop_mass")
parser.add_argument("lsp_mass")
args = parser.parse_args()

ROOT.RooStats.NumberCountingUtils.BinomialExpZ(1,1,1)

f_signal = ROOT.TFile("signalpoints/signal_"+args.stop_mass+"_"+args.lsp_mass+".output.root")
f_W = ROOT.TFile("W.output.root")
f_Z = ROOT.TFile("Z.output.root")
f_top = ROOT.TFile("top.output.root")
f_ttV = ROOT.TFile("ttV.output.root")
f_singletop = ROOT.TFile("singletop.output.root")

#creating list of histogram attributes for each variable
h_att_list = []

njets = hist_attributes("h_njets", "Number of total jets", 0, 20, 1)
h_att_list.append(njets)
nnonbjets = hist_attributes("h_nnonbjets", "Number of non-b-jets", 0, 20, 1)
h_att_list.append(nnonbjets)
nbjets = hist_attributes("h_nbjets","Number of b-jets", 0, 5, 1)
h_att_list.append(nbjets)

met = hist_attributes("h_met", "Missing E_t", 0, 2000, 100)
h_att_list.append(met)
sumet = hist_attributes("h_sumet", "Sum of transverse momentum", 0, 5000, 100)
h_att_list.append(sumet)
top1mass = hist_attributes("h_top1mass", "Top 1 mass", -2000, 2000, 100)
h_att_list.append(top1mass)
drbb = hist_attributes("h_drbb", "DRBB", 0, 5, 100)
h_att_list.append(drbb)

antikt12m0 = hist_attributes("h_antikt12m0", "AntiKt12M_0", 0, 1000, 100)
h_att_list.append(antikt12m0)
antikt12m1 = hist_attributes("h_antikt12m1", "AntiKt12M_1", 0, 1000, 100)
h_att_list.append(antikt12m1)
antikt8m1 = hist_attributes("h_antikt8m1", "AntiKt8M_1", 0, 1000, 100)
h_att_list.append(antikt8m1)
antikt8m0 = hist_attributes("h_antikt8m0", "AntiKt8M_0", 0, 1000, 100)
h_att_list.append(antikt8m0)

#for each variable:
for h_att in h_att_list:
    #get histogram for each process, then scale
    h_signal = f_signal.Get(h_att.hist_name)
    h_W = f_W.Get(h_att.hist_name)
    h_Z = f_Z.Get(h_att.hist_name)
    h_top = f_top.Get(h_att.hist_name)
    h_ttV = f_ttV.Get(h_att.hist_name)
    h_singletop = f_singletop.Get(h_att.hist_name)

    h_signal.Scale(3000)
    h_W.Scale(3000)
    h_Z.Scale(3000)
    h_top.Scale(3000)
    h_ttV.Scale(3000)
    h_singletop.Scale(3000)

    h_totalbackground = h_W + h_Z + h_top + h_ttV + h_singletop

    #making a list of cuts for the variable
    cuts = []
    i = h_att.start
    while i <= h_att.stop:
        cuts.append(i)
        i += h_att.step
#    cuts = np.linspace(h_att.start, h_att.stop, h_att.step)

    #creating histogram for significance against cuts on this variable
    h_cuts = ROOT.TH1F('cuts', 'cuts;'+h_att.x_axis_title+';significance', h_att.step, h_att.start, h_att.stop)

    #creating spreadsheet for significance against cuts on this variable
    with open("significancecharts/" + h_att.hist_name + "_" + args.stop_mass + "_" + args.lsp_mass + "_cuts.csv", 'wb') as csvfile:
        cutwriter = csv.writer(csvfile)
        cutwriter.writerow(['cut', 'W', 'Z', 'top', 'ttV', 'single top', 'total background', 'signal', 'significance'])

        for cut in cuts:
            W_events = h_W.Integral(h_W.FindBin(cut), 10000)
            Z_events = h_Z.Integral(h_Z.FindBin(cut), 10000)
            top_events = h_top.Integral(h_top.FindBin(cut), 10000)
            ttV_events = h_ttV.Integral(h_ttV.FindBin(cut), 10000)
            singletop_events = h_singletop.Integral(h_singletop.FindBin(cut), 10000)
            totalbg_events = h_totalbackground.Integral(h_totalbackground.FindBin(cut), 10000)
            if totalbg_events == 0:
                continue
            signal_events = h_signal.Integral(h_signal.FindBin(cut), 10000)
            significance = ROOT.RooStats.NumberCountingUtils.BinomialExpZ(signal_events, totalbg_events, 0.15)

            #record best significance
            print("h_att is: ", h_att, " cut is: ", cut)
            if (h_att == nbjets) and (cut == cuts[1]):
                print('the best significance is: ', significance)
                best_significance = significance
            
#            print("Cut at ", cut, h_att.hist_name)
#            print("Background events above cut: ", h_W.Integral(h_totalbackground.FindBin(cut),10000))
#            print("Signal events above cut: ", h_signal.Integral(h_signal.FindBin(cut),10000))
#            print("Significance: ", ROOT.RooStats.NumberCountingUtils.BinomialExpZ(h_signal.Integral(h_signal.FindBin(cut),10000), h_totalbackground.Integral(h_totalbackground.FindBin(cut),10000), 0.15))
#            print(" ")
            cutwriter.writerow([cut, W_events, Z_events, top_events, ttV_events, singletop_events, totalbg_events, signal_events, significance])
            h_cuts.Fill(cut,significance)

        

    c_nbjets = ROOT.TCanvas()

    h_cuts.Draw("hist")

    c_nbjets.Print("significancegraphs/Significance"+h_att.tag+"_"+h_att.hist_name+"_"+args.stop_mass+"_"+args.lsp_mass+".pdf")

    
#write best significance to a new csv
with open("best_significance.csv", 'ab') as sfile:
    swriter = csv.writer(sfile)
    swriter.writerow([args.stop_mass, args.lsp_mass, best_significance])

#check table
#repeat signal points
#move other cuts
#@1600, 1
