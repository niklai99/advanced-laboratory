/*
COMPILATION: g++ createRootFile.cpp -o main `root-config --cflags --glibs`
USAGE: ./main [runDay]
    runDay: 2 or 3
DESCRIPTION: This program reads the data from the .root files and saves the data that corresponds to different board-channel combinations into different TTrees in a new .root file.
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>

#include "TFile.h"
#include "TTree.h"

// struct to store the data
struct Data {
    UShort_t  Channel;
    ULong64_t Timestamp;
    UShort_t  Board;
    UShort_t  Energy;
    UShort_t  EnergyShort;
    UInt_t    Flags;
};


// function to read the data from the .root files
std::vector<Data> readData(const std::string &inputFileName) {
    // open the .root files
    TFile *inputFile = new TFile(inputFileName.c_str());

    // get the TTree objects
    TTree *inputTree = (TTree*)inputFile->Get("Data_R;");

    // create a vector of structs to store the data
    std::vector<Data> data;

    // create a struct to store the data temporarily
    Data temp;

    // set the branch addresses
    inputTree->SetBranchAddress("Channel", &temp.Channel);
    inputTree->SetBranchAddress("Timestamp", &temp.Timestamp);
    inputTree->SetBranchAddress("Board", &temp.Board);
    inputTree->SetBranchAddress("Energy", &temp.Energy);
    inputTree->SetBranchAddress("EnergyShort", &temp.EnergyShort);
    inputTree->SetBranchAddress("Flags", &temp.Flags);

    // loop over the TTree objects and fill the data into the vector of structs
    for (int i = 0; i < inputTree->GetEntries(); i++) {
        inputTree->GetEntry(i);
        data.push_back(temp);
    }

    // close the .root files
    inputFile->Close();

    return data;
}

// function to sort the data according to the timestamp
bool sortData(const Data &a, const Data &b) {
    return a.Timestamp < b.Timestamp;
}

void setBranchAddresses(TTree *outputTree, Data &temp) {
    outputTree->Branch("Channel", &temp.Channel);
    outputTree->Branch("Timestamp", &temp.Timestamp);
    outputTree->Branch("Board", &temp.Board);
    outputTree->Branch("Energy", &temp.Energy);
    outputTree->Branch("EnergyShort", &temp.EnergyShort);
    outputTree->Branch("Flags", &temp.Flags);
}


// file names
const std::string inputFileName_1 = "./data/DataR_4Hebeam_run_targetRelocated_7.root";
const std::string inputFileName_2 = "./data/DataR_4Hebeam_day3.root";

const std::string outputFileName_1 = "./data/beam-analysis-day2.root";
const std::string outputFileName_2 = "./data/beam-analysis-day3.root";



int main(int argc, char *argv[]) {

    // read runDay from arguments
    int runDay = atoi(argv[1]);

    // file names
    std::string inputFileName;
    std::string outputFileName;

    std::cout << "Run day: " << runDay << std::endl;

    // check that the runDay is valid and set the file names accordingly
    if (runDay==2) {inputFileName = inputFileName_1; outputFileName = outputFileName_1;}
    else if (runDay==3) {inputFileName = inputFileName_2; outputFileName = outputFileName_2;}
    else {
        std::cout << "Invalid run day" << std::endl;
        return 0;
    }
    
    std::cout << "Reading data from " << inputFileName << "..." << std::endl;
    // read the data from the .root files
    std::vector<Data> data = readData(inputFileName); // CHANGE THIS TO READ THE DATA FROM THE SECOND FILE

    std::cout << "Sorting data..." << std::endl;
    // sort the data according to the timestamp
    std::sort(data.begin(), data.end(), sortData);
    
    // create a new .root file to store the data
    TFile *outputFile = new TFile(outputFileName.c_str(), "RECREATE"); // CHANGE THIS TO WRITE THE DATA TO THE SECOND FILE

    TTree *outputTree_1 = new TTree("labr-b", "labr-b");
    TTree *outputTree_2 = new TTree("labr-a", "labr-a");
    TTree *outputTree_3 = new TTree("clyc", "clyc");
    TTree *outputTree_4 = new TTree("plastic", "plastic");

    // create a struct to store the data temporarily
    Data temp_1;
    Data temp_2;
    Data temp_3;
    Data temp_4;

    // set the branch addresses
    setBranchAddresses(outputTree_1, temp_1);
    setBranchAddresses(outputTree_2, temp_2);
    setBranchAddresses(outputTree_3, temp_3);
    setBranchAddresses(outputTree_4, temp_4);


    std::cout << "Filling new TTrees..." << std::endl;
    // loop over the vector of structs and fill the data into the TTrees
    for (int i = 0; i < data.size(); i++) {
        // Labr-b
        if (data[i].Board == 1 && data[i].Channel == 0) {
            temp_1 = data[i];
            outputTree_1->Fill();
        }
        // Labr-a
        else if (data[i].Board == 1 && data[i].Channel == 1) {
            temp_2 = data[i];
            outputTree_2->Fill();
        }
        // Clyc
        else if (data[i].Board == 1 && data[i].Channel == 2) {
            temp_3 = data[i];
            outputTree_3->Fill();
        }
        // Plastic
        else if (data[i].Board == 1 && data[i].Channel == 3) {
            temp_4 = data[i];
            outputTree_4->Fill();
        }
    }

    std::cout << "Writing TTrees..." << std::endl;
    // write the TTrees to the output .root file
    outputTree_1->Write();
    outputTree_2->Write();
    outputTree_3->Write();
    outputTree_4->Write();

    // close the .root files
    outputFile->Close();

    std::cout << "Done!" << std::endl;

    return 0;
}