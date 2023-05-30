# MareyMap
A pipeline to map markers from a genetic map to a genome assembly

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

Program:<br /><br />
&nbsp;&nbsp;&nbsp;BLAST+ <br /><br />
    
Files:<br /><br />
&nbsp;&nbsp;&nbsp;Fasta file with the genetic markers to align to the genome<br />
&nbsp;&nbsp;&nbsp;Genome file (fasta format)<br />
&nbsp;&nbsp;&nbsp;Tab-delimited genetic map file (column can be specified in the script)<br /><br />

<!-- usage -->
## Usage

1) Generate the blast database:<br /><br />
&nbsp;&nbsp;&nbsp;makeblastdb -in genome.fasta -dbtype nucl<br />
    
2) Align markers to the genome (format 6 required -- see example):<br /><br />
&nbsp;&nbsp;&nbsp;blastn -task megablast -query markers.fasta -db genome.fasta -outfmt 6 -out markers.vs.genome.aln <br />

3) Filter alignments:<br /><br />
&nbsp;&nbsp;&nbsp;python Filter_Alignments_Blast_Fmt6_ver1.0.py -aln_file markers.vs.genome.aln -min_per 80 > markers.vs.genome.filtered.aln <br /><br />
&nbsp;&nbsp;&nbsp;help (and further explanations): python Filter_Alignments_Blast_Fmt6_ver1.0.py -h<br />
    
4) Generate Marey map<br /><br />
&nbsp;&nbsp;&nbsp;python MatchingMarkers.v1.0.py -aln markers.vs.genome.filtered.aln -map Map.txt -pos 1 > MareyMap.txt<br /><br />
&nbsp;&nbsp;&nbsp;help (and further explanations): python MatchingMarkers.v1.0.py -h<br />

<!-- license -->
## License 

Distributed under the MIT License.
