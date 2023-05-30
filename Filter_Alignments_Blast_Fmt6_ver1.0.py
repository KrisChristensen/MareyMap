##########################################################
### Import Necessary Modules

import argparse		               #provides options at the command line
import sys		               #take command line arguments and uses it in the script
import gzip		               #allows gzipped files to be read
import re		               #allows regular expressions to be used
from random import shuffle             #allows randomization of a list

##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="Filter an alignment file based on criteria and add info to synteny info.")
parser.add_argument("-aln_file", help = "The location of the alignment file in outfmt=6", default=sys.stdin, required=True)
parser.add_argument("-min_per", help = "The minimum percent id to keep an alignment (default:0)", default=0)
parser.add_argument("-min_aln", help = "The minimum alignment length to keep an alignment (default:0)", default=0)
args = parser.parse_args()

#########################################################
### Open file (object-oriented programming)

class OpenFile():
    previous_query = "NA"
    previous_loci  = "NA"
    query_list     = []
    loci_list      = {}
    
    ### Opens the file and either directs it to a line-reader for alignment files or fasta files
    def __init__ (self, filename, fileType):
        if re.search(".gz$", filename):
            self.filename = gzip.open(filename, 'rb')
        else:
            self.filename = open(filename, 'r')             
        #print "opened {}".format (filename)
        if fileType == "aln":
            self.readLinesAln()

    ### Reads alignment files, but only those which pass a minimum threshold
    ### Alignments are also grouped by the query sequence, and then sent to another method
    def readLinesAln(self):
        sys.stderr.write("\n{}\n\n".format("Started to read lines"))
        for line in self.filename:
            line = line.rstrip('\n')
            query,subject,per_id,aln_len,mismatch,gap,qstart,qend,sstart,send,evalue,bit = line.split("\t")
            full_query = query.split(":")
            ###Only analyzes alignments longer and better than minimum alignment scores
            if float(per_id) >= float(args.min_per) and int(aln_len) >= int(args.min_aln):
                if OpenFile.previous_query == "NA":
                    OpenFile.previous_query = query
                    OpenFile.previous_locus = full_query[0]
                    OpenFile.query_list.append(line)
                else:
                    if OpenFile.previous_query == query:
                        OpenFile.query_list.append(line)
                    else:
                        if len(OpenFile.query_list) > 0:
                            self.alignmentAnalysis(OpenFile.previous_locus)
                        OpenFile.query_list = []
                        OpenFile.query_list.append(line)
                        OpenFile.previous_locus = full_query[0]
                        OpenFile.previous_query = query
        self.filename.close()
        self.alignmentAnalysis(OpenFile.previous_locus)

    def alignmentAnalysis(self, l):
        self.locus = l
        self.bestBit = 0
        self.bestCount = 0
        sys.stderr.write("{}".format("\n"))
        for aln in OpenFile.query_list:
            query,subject,per_id,aln_len,mismatch,gap,qstart,qend,sstart,send,evalue,bit = aln.split("\t")
            if float(bit) >= self.bestBit:
                self.bestBit = float(bit)
                self.bestCount += 1
        for aln in OpenFile.query_list:
            query,subject,per_id,aln_len,mismatch,gap,qstart,qend,sstart,send,evalue,bit = aln.split("\t")
            if float(bit) == self.bestBit and int(self.bestCount) == 1:
                sys.stderr.write("\t\tlocus:{}**printed\n".format(aln))
                print ("{}".format(aln))
            else:
                sys.stderr.write("\t\tlocus:{}\n".format(aln))
       
if __name__ == '__main__':            
    open_aln = OpenFile(args.aln_file, "aln")
