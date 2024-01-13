# Useful one-liners for computational biology

## Convert 

### Remove duplicates from blast, sword, or diamond file (Top Hit keep) based on column

#### Based on first column
```
awk '!a[$1]++ file
```

#### Based on second column
```
awk '!a[$2]++ file
```

### Convert fastq to fasta

#### Option 1
```
sed -n '1~4s/^@/>/p;2~4p' file.fastq >file.fasta
```

#### Option 2
```
sed '/^@/!d;s//>/;N' file.fastq >file.fasta
```

#### Option 3
```
awk '/^@/{gsub(/^@/,">",$1);print;getline;print}' file.fastq >file.fna
```

### Convert multiline fasta to single line 

#### Option 1
```
perl -pe '/^>/ ? print "\n" : chomp' multi-line.fasta >single-line.fasta
``` 

#### Option 2
```
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < multi-line.fasta >single-line.fasta
``` 

#### Option 3
```
perl -pe 'chomp unless /^>/' multi-line.fasta >single-line.fasta
``` 

#### Option 4
```
awk '/^>/ { if(NR>1) print "";  printf("%s\n",$0); next; } { printf("%s",$0);}  END {printf("\n");}' < multi-line.fasta >single-line.fasta
```

#### Option 5
```
awk 'BEGIN{RS=">"}NR>1{sub("\n","\t"); gsub("\n",""); print RS$0}' < multi-line.fasta >single-line.fasta
```

#### Option 6
```
perl -pe '$. > 1 and /^>/ ? print "\n" : chomp' multi-line.fasta >single-line.fasta
```

### Change the headers of a fasta file with names within a list (names.txt)
```
paste <(ls *.faa) names.txt | while read -r file name; do
  echo "sed -E 's/^>(.*)$/>'\"${name}_\1/\" \"$file\" > \"$(basename "$file" .faa)_re.faa\""
done >> headers.sh
```

### Remove contigs based on header (after transform to single line)
```
grep -A1 -f list_to_filter contigs.fasta >rm_contigs.fasta
grep -v -f rm_contigs.fasta contigs.fasta >output.fasta
```

### Convert multi-line fasta to a single line fasta (contig files)
```
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < file.fa > out.fa
```

### Convert csv to tsv 
```
sed -E 's/("([^"]*)")?,/\2\t/g' file.csv >> file.tsv
```

### Convert Sam to fastq
```
cat file.sam | grep -v ^@ | awk '{print "@"$1"\n"$10"\n+\n"$11}' > file.fastq
```

### Copy many files from many directories
```
find . -name "*.gff" -type f -exec cp {} ./. \;
```

### Split with file name
```
split -d -a1 -b 10M --additional-suffix=.tsv metadata.tsv metadata
split -d -a1 -b 10M --additional-suffix=.fna seq.fna seq
```

### Basename regular expressions
```
for i in *fna; do echo command "$i" $(basename $i | sed 's/_ViralMultiSegProj[0-9]\{5\}_genomic.fna//' | sed 's/_ViralMultiSegProj[0-9]\{6\}_genomic.fna//' | sed 's/_ASM[0-9]\{6\}v1_genomic.fna//' | sed 's/_ASM[0-9]\{7\}v1_genomic.fna//' | sed 's/_ASM[0-9]\{6\}v3_genomic.fna//' )/ >>split.sh; done
```

## Count 

### AWK for rapid fastq read count
```
awk '{s++}END{print s/4}' file.fastq
```

### Rapid fastq read count (.gz)
```
zcat file.fastq.gz | echo $((`wc -l`/4))
```

### Grep to count a fasta file

#### Option 1
```
grep ">" file.fasta -c
```

#### Option 2
```
grep ">" file.fasta | wc -l 
```

### Grep to count a fastq file

#### Option 1
```
grep "@" file.fastq -c
```

#### Option 2
```
grep "@" file.fastq | wc -l 
```

### Rename many files

#### 
```
for i in *NAME*; do mv $i ${i/NAME/NEW_NAME}; done;
```
## BioAWK Commands

## SED Commands

### Convert fastq to fna
```
sed -n '1~4s/^@/>/p;2~4p' file.fastq >file.fna
```

### Remove spaces in a fasta file
```
sed -r ‘s/\s+//g’
```

### Remove empty lines
```
sed '/^$/d' 
```

### Make uppercase text in a fasta file
```
sed 's/[a-z]/\U&/g'
```

### Make lowercase text in a fasta file
```
sed 's/[A-Z]/\L&/g'
``` 

### Add a tab after the first space
```
sed 's/^[ ]*\([^ ]*\) /\1\t/' file.txt >New_file.txt
```

## SAMTOOLS

### Convert Sam to Unmapped (sam)
```
samtools view -S -f 4 file.bam >file_unmapped.sam
```

### Convert Sam to Mapped (sam)
```
samtools view -S -F 4 file.sam >file_mapped.sam
```

### Convert Bam to Unmapped (bam)
```
samtools view -b -f 4 file.bam >file_unmapped.bam
```

### Convert Bam to Mapped (bam)
```
samtools view -b -F 4 file.bam >file_mapped.bam
```

### Convert Bam to fastq
```
samtools fastq file.bam >file.fastq
```

## MAPPING

## Bowtie2 

### Build Bowtie2 db
```
bowtie2-build database.fa db
```

### Map paired end/single end (.fq, .fastq, .gz)

#### Global 

##### Paired-end data (Illumina only)
```
bowtie2 -p number of threads -x db -1 R1.fastq -2 R2.fastq -S global.sam --very-sensitive
```

##### Single-end data (Illumina only)
```
bowtie2 -p number of threads -x db -q R1.fastq -S global.sam --very-sensitive
```

#### Local

##### Paired-end data (Illumina only)
```
bowtie2 -p number of threads -x db -1 1.fastq -2 2.fastq -S local.sam --very-sensitive-local
```

##### Single-end data (Illumina only)
```
bowtie2 -p number of threads -x db -q R1.fastq -S local.sam --very-sensitive-local` 
```

## Phylogenetics

### MAFFT

#### Local
```
mafft --localpair --maxiterate 1000 --clustalout file.fasta >file_local.clust
```

#### Global
```
mafft --globalpair --maxiterate 1000 --clustalout file.fasta >file_global.clust
```

### IQ-Tree2

#### Protein based Tree
```
iqtree2 -s file_local.clust -st AA -m TEST -bb 1000 -alrt 1000
```

#### Nucleotide (DNA) based Tree
```
iqtree2 -s file_local.clust -st DNA -m TEST -bb 1000 -alrt 1000
```

### Tree annotator 
```
tree_annotator.py annotation.csv treefile output
```

### Contact 
The point-of-contact for this project is [Dr. Richard Allen White III](https://github.com/raw-lab/).<br />
If you have any questions or feedback, please feel free to get in touch by email. 
Dr. Richard Allen White III - raw937@gmail.com or rwhit101@uncc.edu  <br />
Or [open an issue](https://github.com/raw-lab/oneliners/issues).
