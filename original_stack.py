import argparse
import ROOT
import time

class hist_attributes:
    def __init__(self, name="", title=""):
        self.hist_name = name
        self.x_axis_title = title
        self.tag = ""

parser = argparse.ArgumentParser()
parser.add_argument("stop_mass")
parser.add_argument("lsp_mass")
args = parser.parse_args()
processes = ["signal", "W", "Z", "top", "ttV", "singletop"]
colour_list = [ROOT.kRed, ROOT.kOrange, ROOT.kYellow, ROOT.kSpring, ROOT.kTeal, ROOT.kBlue]

h_att_list = []

njets = hist_attributes("h_njets", "Number of total jets")
h_att_list.append(njets)
nnonbjets = hist_attributes("h_nnonbjets", "Number of non-b-jets")
h_att_list.append(nnonbjets)
nbjets = hist_attributes("h_nbjets","Number of b-jets")
h_att_list.append(nbjets)

met = hist_attributes("h_met", "Missing E_t")
h_att_list.append(met)
sumet = hist_attributes("h_sumet", "Sum of transverse momentum")
h_att_list.append(sumet)
top1mass = hist_attributes("h_top1mass", "Top 1 mass")
h_att_list.append(top1mass)
drbb = hist_attributes("h_drbb", "DRBB")
h_att_list.append(drbb)

antikt12m0 = hist_attributes("h_antikt12m0", "AntiKt12M_0")
h_att_list.append(antikt12m0)
antikt12m1 = hist_attributes("h_antikt12m1", "AntiKt12M_1")
h_att_list.append(antikt12m1)
antikt8m1 = hist_attributes("h_antikt8m1", "AntiKt8M_1")
h_att_list.append(antikt8m1)
antikt8m0 = hist_attributes("h_antikt8m0", "AntiKt8M_0")
h_att_list.append(antikt8m0)

for h_att in h_att_list:
    hist_list = []
    cumulative_hist_list = []
    file_list = []

    print(h_att.hist_name)
    for process in processes:
        print(process)
        if process == "signal":
            file_list.append(ROOT.TFile("originalsignalpoints/original_" + process + "_" + args.stop_mass + "_" + args.lsp_mass + ".output.root"))
        else:
            file_list.append(ROOT.TFile("original_" + process + ".output.root"))            

    paired_list = zip(processes, file_list)

    for process, file in paired_list:
        hist_list.append(file.Get(h_att.hist_name))

    for hist in hist_list:
        hist.Scale(3000)

    cumulative_hist_list.append(hist_list[0])

    for i in range(1, len(hist_list)):
        cumulative_hist_list.append(hist_list[i])
        for j in range(1,i):
            cumulative_hist_list[i] += hist_list[j]

    c_met = ROOT.TCanvas()

    cumulative_hist_list[5].SetFillColor(colour_list[5])
    cumulative_hist_list[5].Draw("hist")
    cumulative_hist_list[5].SetXTitle(h_att.x_axis_title)
    cumulative_hist_list[5].SetYTitle("Counts")

    for i in range(5, -1, -1):
        cumulative_hist_list[i].SetFillColor(colour_list[i])
        cumulative_hist_list[i].Draw("histsame")

    legend = ROOT.TLegend(0.6,0.65,0.8,0.8)
    for i in range(6):
        legend.AddEntry(cumulative_hist_list[i], processes[i])
    legend.Draw()
    c_met.gStyle.SetOptStat(0)
    c_met.SetLogy()
    c_met.Print("originalstackgraphs/original_stack"+h_att.tag+"_"+h_att.hist_name+"_"+args.stop_mass+"_"+args.lsp_mass+".pdf")

    time.sleep(0.5)
