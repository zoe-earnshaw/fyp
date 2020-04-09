#! /usr/bin/env python 
import argparse
import ROOT, sys

#take stop and lsp mass for chosen signal point from input
parser = argparse.ArgumentParser()
parser.add_argument("stop_mass")
parser.add_argument("lsp_mass")
args = parser.parse_args()

#listing signal and background processes
process_names = ['signalpoints/signal*directTT*' + args.stop_mass + '_' + args.lsp_mass + '.*', 'singletop','top','ttV', 'W','Z']

#for each process:
for name in process_names:
    print(name)
    
    #creating Tchain
    testchain = ROOT.TChain("StopZeroLeptonUpgrade__ntuple")
    #adding root files for given process
    testchain.Add("/lustre/scratch/epp/atlas/iv41/OUTPUT/UpgradeAnalysisOutput/LargeDM/" + name + "*_NTUP.root")
   
    #creating output file
    file_name = name
    if "signal" in name:
        file_name = "original_signal" + "_" + args.stop_mass + "_" + args.lsp_mass
    outputfile = ROOT.TFile("original_" + file_name + ".output.root", "recreate")

    print(testchain.GetEntries())

    #creating histograms for variables
    h_met = ROOT.TH1F("h_met"," ",100,0,2000)
    h_nbjets = ROOT.TH1F("h_nbjets"," ",10,0,10)
    h_njets = ROOT.TH1F("h_njets"," ",20,0,20)
    h_nnonbjets = ROOT.TH1F("h_nnonbjets"," ",20,0,20)
    h_top1mass = ROOT.TH1F("h_top1mass"," ",100,-2000,2000)
    h_sumet = ROOT.TH1F("h_sumet"," ",100,0,5000)
    h_antikt8m0 = ROOT.TH1F("h_antikt8m0"," ",100,0,1000)
    h_antikt8m1 = ROOT.TH1F("h_antikt8m1"," ",100,0,1000)
    h_antikt12m0 = ROOT.TH1F("h_antikt12m0"," ",100,0,1000)
    h_antikt12m1 = ROOT.TH1F("h_antikt12m1"," ",100,0,1000)
    h_drbb = ROOT.TH1F("h_drbb"," ",100,0,5)

    #should have 2 signals at different delta m

    #applying cuts
    counter = 0
    for entry in testchain:
        #filling variable hists & weighting without cuts
        h_met.Fill(entry.Met, entry.GlobalWeight)
        h_nbjets.Fill(entry.NBJets, entry.GlobalWeight)
        h_njets.Fill(entry.NJets, entry.GlobalWeight)
        h_nnonbjets.Fill(entry.NNonBJets, entry.GlobalWeight)
        h_top1mass.Fill(entry.top1M, entry.GlobalWeight)
        h_sumet.Fill(entry.SumEt, entry.GlobalWeight)
        h_antikt8m0.Fill(entry.AntiKt8M_0, entry.GlobalWeight)
        h_antikt8m1.Fill(entry.AntiKt8M_1, entry.GlobalWeight)
        h_antikt12m0.Fill(entry.AntiKt12M_0, entry.GlobalWeight)
        h_antikt12m1.Fill(entry.AntiKt12M_1, entry.GlobalWeight)
        h_drbb.Fill(entry.DRBB, entry.GlobalWeight)

        counter += 1
        if counter%1000 == 0:
            print("Counter = ", counter)

    outputfile.Write()
    outputfile.Close()

#TDirectory to structure
