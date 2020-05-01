#! /usr/bin/env python 
import argparse
import ROOT, sys
import csv

#take stop and lsp mass for chosen signal point from input
parser = argparse.ArgumentParser()
parser.add_argument("stop_mass")
parser.add_argument("lsp_mass")
args = parser.parse_args()

#listing signal and background processes
process_names = ['signal*directTT*' + args.stop_mass + '_' + args.lsp_mass + '.*', 'singletop','top','ttV', 'W','Z']

#for each process:
for name in process_names:
    print(name)
        
    if 'signal' in name:
        is_signal = 1
        name = "signal_"+ args.stop_mass + "_" + args.lsp_mass
    else:
        is_signal = 0
    
    with open("csvfile/" + name + "_data_" + ".csv", 'wb') as csvfile:
        cutwriter = csv.writer(csvfile)
        cutwriter.writerow(['met','njets','nbjets','nnonbjets','top1mass','sumet','antikt8m0','antikt8m1','antikt12m0','antikt12m1','drbb','is_signal'])

        #creating Tchain
        testchain = ROOT.TChain("StopZeroLeptonUpgrade__ntuple")
        #adding root files for given process
        testchain.Add("/lustre/scratch/epp/atlas/iv41/OUTPUT/UpgradeAnalysisOutput/LargeDM/" + name + "*_NTUP.root")
   
        #creating output file

        print(testchain.GetEntries())

        #applying cuts
        counter = 0
        for entry in testchain:
            if (entry.NBJets < 2):
                continue
                #writing to csv, if entry passes the cuts
        
            cutwriter.writerow([entry.Met, entry.NBJets, entry.NJets, entry.NNonBJets, entry.top1M, entry.SumEt, entry.AntiKt8M_0, entry.AntiKt8M_1, entry.AntiKt12M_0, entry.AntiKt12M_1, entry.DRBB, is_signal])

            counter += 1
            if counter%1000 == 0:
                print("Counter = ", counter)
