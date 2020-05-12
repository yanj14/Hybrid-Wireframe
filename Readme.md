# **Hybrid wireframe origami**
## About
Here we deposit two scripts to generate hybrid wireframe origami. We designed the basic 3-arm, 4-arm and 6-arm structures. **M13 p8064 ssDNA** was the scaffold and **staples (short ssDNA oligos)** were used to establish the shapes and patterns.

Each staple contains several fragments (>=2) and two of them directly bind to the scaffold. To generate variants of those basic structures, the two segments that bind directly to p8064 were not changed and between them, different linkers were inserted such as short stretch of ssDNA, dsDNA.

The two scripts here first index p8064 and obtain the coordinate of staple segments that directly bind p8064. Then the linker sequence file that specify the connection patterns of linkers with staples is loaded and all staple sequences are ouput in a .txt file.

## Running the python script
1. Download the script from github.

        git clone

2. In Powershell (Windows) or Terminal (Linux, MacOS), change directory to the downloaded script folder. For example:

        cd /home/jy15/Desktop/6arm_wireframe_origami

3. Run the scripts

        python3 6arm_staples.py --outdir <output path> --linker <linker sequence path> --dsOption <1/0>


## Options
`--outdir <output path>`  Path to the folder where the generated staple sequence file will be saved. Default is current working directory.

`--linker <linker sequence path>`  Path to the linker sequence file. Default is empty string which tells the script to use the defult 'TT' linker to connect two staple segments.

`--dsOption <1/0>` To specify if the linker should be inserted as ssDNA (0) or dsDNA (1). Default is ssDNA (0).

## Input requirement###
The linker sequence file is a tab-delimited txt file which consists of first three mandatory columns and one optional fourth column. The first three are the 1st staple segment id., the 2nd staple segment id. and the linker sequence. The fourth column is the staple-linker connection pattern.

If linkers are ssDNA, the fourth column is not needed. However, if linkers are dsDNA, then the 1st staple segment will be joint with the linker sequence listed in the same line while the second segment will be joint with the reverse complement of the linker sequence. For dsDNA linker, you also need to specify if the generated staples start or end with the linkers by adding 'start' or 'end' to the fourth column.

**Please be aware that a 'TT' dinucleotide will be automatically added between the linker and the staple segment to provide necessary structural flexibility.**

**All unspecified staple segment pairs will be joint by a 'TT' dinucleotide.**

## Output
The output file is a tab-delimited .txt file consisting of two columns. If the linker between two staple segment is ssDNA then only one staple will be generated. If the linker is dsDNA, then one staple will be generated for each segment. The first column is staple or staple segment id.(marked in basic structures) and the second column is the staple sequence.


## Demo
1. Demo1 6-arm wireframe origami
        python3 6arm_staples.py --outdir ./Demo_6arm/

2. Demo2 6-arm wireframe origami variant 1
        python3 6arm_staples.py --outdir ./Demo_6arm_V1/ --linker ./Demo_6arm_V1/6arm_V1_linker.txt/

3. Demo3 6-arm wireframe origami variant 3
        python3 6arm_staples.py --outdir ./Demo_6arm_V3/ --linker ./Demo_6arm_V3/6arm_V3_linker.txt/ --dsOption 1

4. Demo3 6-arm wireframe origami variant 3_32nt
        python3 6arm_staples.py --outdir ./Demo_6arm_V3_32nt/ --linker ./Demo_6arm_V3_32nt/6arm_V3_32nt_linker.txt/  -dsOption 1

5. Demo4 3-arm wireframe origami
