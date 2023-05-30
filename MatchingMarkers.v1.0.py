##########################################################
### Import Necessary Modules

import argparse		               #provides options at the command line
import sys		               #take command line arguments and uses it in the script
import gzip		               #allows gzipped files to be read
import re		               #allows regular expressions to be used


##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="A script to get filtered genomic positions from a blast6 format alignment file and put in a Genetic map file")
parser.add_argument("-aln", help = "The location of the blast 6 format alignment file", default=sys.stdin, required=True)
parser.add_argument("-map", help = "The location of the genetic map in tab-delimited file (marker must be first and must have header)", default=sys.stdin, required=True)
parser.add_argument("-pos", help = "The column position of the genetic marker, default = 0 (first column - zero based)", default=0)
args = parser.parse_args()


class CommonVariables():
    geneticMarkers = {}

class OpenFile():
    ### Opens the file and either directs it to a line-reader for alignment files
    def __init__ (self, filename, fileType):
        """Reads in gzipped and regular files and sends to appropriate reader"""
        if re.search(".gz$", filename):
            self.filename = gzip.open(filename, 'rb')
        else:
            self.filename = open(filename, 'r')             
        if fileType == "aln":
            sys.stderr.write ("Opened aln file: {}\n\n".format (filename))
            ReadAln(self.filename)
        if fileType == "map":
            sys.stderr.write ("Opened map file: {}\n\n".format (filename))
            ReadMap(self.filename)

class ReadAln():
    ### Reads alignment files
    def __init__ (self, f):
        """Reads in the alignment file"""
        ###75037_x1	NC_042549.1	97.87	94	2	0	1	94	16625156	16625063	6e-39	163
        for self.line in f:
            self.line = self.line.rstrip('\n')
            self.marker, self.chrom, self.pid, self.length = self.line.split("\t")[0:4]
            self.positionSt = self.line.split("\t")[8]
            self.positionEn = self.line.split("\t")[9]
            CommonVariables.geneticMarkers[self.marker] = "{}\t{}\t{}\t{}\t{}".format(self.chrom, self.positionSt, self.positionEn, self.pid, self.length)
        f.close()

class ReadMap():
    ### Reads alignment files
    def __init__ (self, f):
        """Reads in the map file"""
        #print "{}\t{}".format(f.readline().rstrip('\n'), "Marker\tChrom\tPercentID\tLength")
        for self.line in f:
            self.line = self.line.rstrip('\n')
            self.marker = self.line.split()[int(args.pos)]
            if self.marker in CommonVariables.geneticMarkers:
                print ("{}\t{}".format(self.line, CommonVariables.geneticMarkers[self.marker]))
            else:
                print ("{}\t{}".format(self.line, "NA\tNA\tNA\tNA"))
        f.close()
      
if __name__ == '__main__':            
    open_aln = OpenFile(args.aln, "aln")
    open_map = OpenFile(args.map, "map")
