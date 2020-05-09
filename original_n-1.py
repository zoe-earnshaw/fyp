import ROOT
import argparse
import csv

class hist_attributes:
    def __init__(self, name="", title="", start=0, stop=100, step=10):
        self.hist_name = name
        self.x_axis_title = title
        self.stop = stop
        self.start = start
        self.step = step
        self.tag = ""

ROOT.RooStats.NumberCountingUtils.BinomialExpZ(1,1,1)

parser = argparse.ArgumentParser()
parser.add_argument("stop_mass")
parser.add_argument("lsp_mass")
args = parser.parse_args()

process_names = ['signal*directTT*' + args.stop_mass + '_' + args.lsp_mass + '.*', 'singletop','top','ttV', 'W','Z']

for name in process_names:
    print(name)
    testchain = ROOT.TChain ("StopZeroLeptonUpgrade__ntuple")
    testchain.Add("/lustre/scratch/epp/atlas/iv41/OUTPUT/UpgradeAnalysisOutput/LargeDM/" + name + "*_NTUP.root")
    file_name = name
    if "signal" in name:
        file_name = "signal"
    outputfile = ROOT.TFile("original_" + file_name + "_N-1_" + args.stop_mass + "_" + args.lsp_mass + ".output.root", "recreate")

    print(testchain.GetEntries())

    h_met = ROOT.TH1F("h_met"," ",100,0,2000)
    h_nbjets = ROOT.TH1F("h_nbjets"," ",10,0,10)
    h_sumet = ROOT.TH1F("h_sumet"," ",100,0,5000)
    h_antikt8m0 = ROOT.TH1F("h_antikt8m0"," ",100,0,1000)
    h_antikt8m1 = ROOT.TH1F("h_antikt8m1"," ",100,0,1000)
    h_antikt12m1 = ROOT.TH1F("h_antikt12m1"," ",100,0,1000)

    counter = 0
    for entry in testchain:
        if (entry.AntiKt12M_1 > 100) and \
                (entry.AntiKt12M_1 < 250) and \
                (entry.SumEt > 1500) and \
                (entry.AntiKt8M_0 > 150) and \
                (entry.AntiKt8M_1 > 150) and \
                (entry.Met > 800):
            h_nbjets.Fill(entry.NBJets, entry.GlobalWeight)

        if (entry.NBJets > 2) and \
                (entry.SumEt > 1500) and \
                (entry.AntiKt8M_0 > 150) and \
                (entry.AntiKt8M_1 > 150) and \
                (entry.Met > 800):
            h_antikt12m1.Fill(entry.AntiKt12M_1, entry.GlobalWeight)


        if (entry.NBJets > 2) and \
                (entry.AntiKt12M_1 > 100) and \
                (entry.AntiKt12M_1 < 250) and \
                (entry.AntiKt8M_0 > 150) and \
                (entry.AntiKt8M_1 > 150) and \
                (entry.Met > 800):
            h_sumet.Fill(entry.SumEt, entry.GlobalWeight)

        if (entry.NBJets > 2) and \
                (entry.AntiKt12M_1 > 100) and \
                (entry.AntiKt12M_1 < 250) and \
                (entry.SumEt > 1500) and \
                (entry.AntiKt8M_1 > 150) and \
                (entry.Met > 800):
            h_antikt8m0.Fill(entry.AntiKt8M_0, entry.GlobalWeight)

        if (entry.NBJets > 2) and \
                (entry.AntiKt12M_1 > 100) and \
                (entry.AntiKt12M_1 < 250) and \
                (entry.SumEt > 1500) and \
                (entry.AntiKt8M_0 > 150) and \
                (entry.Met > 800):
            h_antikt8m1.Fill(entry.AntiKt8M_1, entry.GlobalWeight)

        if (entry.NBJets > 2) and \
                (entry.AntiKt12M_1 > 100) and \
                (entry.AntiKt12M_1 < 250) and \
                (entry.SumEt > 1500) and \
                (entry.AntiKt8M_0 > 150) and \
                (entry.AntiKt8M_1 > 150):
            h_met.Fill(entry.Met, entry.GlobalWeight)


        counter += 1
        if counter%1000 == 0:
            print("Counter = ", counter)

    outputfile.Write()
    outputfile.Close()


f_signal = ROOT.TFile("originalsignalpoints/original_signal_"+args.stop_mass+"_"+args.lsp_mass+".output.root")
f_W = ROOT.TFile("original_W.output.root")
f_Z = ROOT.TFile("original_Z.output.root")
f_top = ROOT.TFile("original_top.output.root")
f_ttV = ROOT.TFile("original_ttV.output.root")
f_singletop = ROOT.TFile("original_singletop.output.root")

h_att_list = []

nbjets = hist_attributes("h_nbjets","Number of b-jets", 0, 5, 5)
h_att_list.append(nbjets)

met = hist_attributes("h_met", "Missing E_t", 0, 2000, 100)
h_att_list.append(met)
sumet = hist_attributes("h_sumet", "Sum of transverse momentum", 0, 5000, 100)
h_att_list.append(sumet)

antikt12m1 = hist_attributes("h_antikt12m1", "AntiKt12M_1", 0, 1000, 100)
h_att_list.append(antikt12m1)
antikt8m1 = hist_attributes("h_antikt8m1", "AntiKt8M_1", 0, 1000, 100)
h_att_list.append(antikt8m1)
antikt8m0 = hist_attributes("h_antikt8m0", "AntiKt8M_0", 0, 1000, 100)
h_att_list.append(antikt8m0)

for h_att in h_att_list:
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

    cuts = []
    i = h_att.start
    while i <= h_att.stop:
        cuts.append(i)
        i += h_att.step

    h_cuts = ROOT.TH1F('cuts', 'cuts;'+h_att.x_axis_title+';significance', (h_att.stop-h_att.start)/h_att.step, h_att.start, h_att.stop)

    with open(h_att.hist_name+"_cuts.csv", 'wb') as csvfile:
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

            cutwriter.writerow([cut, W_events, Z_events, top_events, ttV_events, singletop_events, totalbg_events, signal_events, significance])

            h_cuts.Fill(cut,significance)


    c_nbjets = ROOT.TCanvas()

    h_cuts.Draw("hist")

    c_nbjets.Print("Significance"+h_att.tag+"_N-1_"+h_att.hist_name+"_"+args.stop_mass+"_"+args.lsp_mass+".pdf")

