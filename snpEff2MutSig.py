#!/usr/bin/env python

import argparse
import os
import sys

class Transcript:
    def __init__(self,geneName,enst,putativeImpact,transcriptLength,annotation):
        putativeImpactDict = {"HIGH":4,"MODERATE":3,"MODIFIER":1,"LOW":2}
        self.geneName = geneName
        self.enst = enst
        self.putativeImpact = putativeImpact
        self.numericPutativeImpact = putativeImpactDict.get(putativeImpact)
        self.transcriptLength = transcriptLength
        self.annotation = annotation
    
    def __repr__(self):
        return "{},{},{}".format(self.enst,self.putativeImpact,self.transcriptLength)
    
    def __cmp__(self,other):
        if self.numericPutativeImpact > other.numericPutativeImpact:
            return 1
        if self.numericPutativeImpact < other.numericPutativeImpact:
            return -1
        if self.numericPutativeImpact == other.numericPutativeImpact:
            if self.transcriptLength > other.transcriptLength:
                return 1
            if self.transcriptLength < other.transcriptLength:
                return -1
            if self.transcriptLength == other.transcriptLength:
                return 0

def get_gene_symbol_and_effect(info):
    
    transcriptList = []
    splittedInfo = info.split(";")
    for infoElement in splittedInfo:
        if infoElement.startswith("ANN"):
            snpEffAnnotation = infoElement[4:]
            break
    transcripts = snpEffAnnotation.split(",")
    for transcript in transcripts:
        splittedTranscript = transcript.split("|")
        transcriptLength = splittedTranscript[11]
        if "/" in transcriptLength:
            transcriptLength = int(transcriptLength.split("/")[1])
        else:
            transcriptLength = 0
        annotation,putativeImpact,geneName,enst = splittedTranscript[1], splittedTranscript[2],splittedTranscript[3],splittedTranscript[6]
        transcriptInstance = Transcript(geneName,enst,putativeImpact,transcriptLength,annotation)
        transcriptList.append(transcriptInstance)
    transcriptList.sort()
    canonicalTranscript = transcriptList[-1]
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert snpEff annotated vcfs to input MutSigCV")

    parser.add_argument('-g', '--genome', action='store', type=file, help="Enter a fasta file containing a reference genome", required=True)
    parser.add_argument("-d", "--directory", help="Enter vcfs directory", required=True, type=str, default=".")
    args = parser.parse_args()

    if os.path.isdir(args.directory) == False:
        sys.exit("Directory {} does not exist".format(args.directory))
    filesInDirectory = os.listdir(args.directory)
    vcfFiles = [f for f in filesInDirectory if f.endswith(".vcf")]
    for vcfName in vcfFiles:
        vcf = open(os.path.join(args.directory,vcfName))
        for line in vcf:
            if not line.startswith("#"):
                splittedLine = line.strip().split("\t")
                chrom,pos,ref,alt,info = splittedLine[0],splittedLine[1],splittedLine[3],splittedLine[4],splittedLine[7]
                get_gene_symbol_and_effect(info)
#                sys.exit()
        vcf.close()
