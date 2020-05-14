# **Hybrid 3-arm wireframe origami**

## About

This script generates the 3-arm wireframe structure and its variants

---

## Running the python script
1. Download the script from github.

        git clone https://github.com/yanj14/Hybrid-Wireframe

2. In Powershell (Windows) or Terminal (Linux, MacOS), change directory to the downloaded script folder. For example:

        cd /Hybrid-Wireframe/3_arm/

3. Run the scripts

        python 3arm_staples.py --outdir <output path> --linker <linker sequence path> --deletion <staples to delete file path>

---

## Options
`--outdir <output path>`  Path to the folder where the generated staple sequence file will be saved. Default is current working directory.

`--linker <linker sequence path>`  Path to the linker sequence file. Default is empty string which tells the script to use the defult 'TT' linker to connect two staple fragments.

`--deletion <staples to delete file path>` Path to the text file specifying staples to be removed. Default is to keep all staples.

`--name <the file name (no format extension)>` The name of the output file. Default is 'Staple_sequences'. 

---

## Input requirements

### Requirements for text files to delete staples

To delete a staple, simply write down the number of the staple to be deleted (one number per line). For example:

    1
    2
    3

### Requirements for linker sequence files

The linker sequence file is a tab-delimited txt file which consists of two columns. The first column is the staple number ID. **(IDs. are marked in the 3_arm figure)** and the second is the linker sequence

**Please be aware** that a 'TT' dinucleotide will be automatically added between the linker and the staple fragment to provide necessary structural flexibility. All  staple fragment pairs without provided linkers will be joint by a 'TT' dinucleotide.

---

## Output
The output file is a tab-delimited .txt file consisting of two columns. The first column is staple IDs. **(IDs. are marked in the 3_arm figure)** and the second column is the staple sequence.

---

## Demo
### Demo1: Basic 3-arm wireframe origami
The 3-arm wireframe structure is illustrated below (also see 3_arm.png).
Linux or MacOS or Windows (powershell/cygWin)

    python 3arm_staples.py --outdir ./ --linker ./3arm_linker.txt

Windows (cmd)

    python 3arm_staples.py --outdir .\ --linker .\3arm_linker.txt 

<img src="https://github.com/yanj14/Hybrid-Wireframe/blob/master/3_arm/3_arm.png" width="650" height="650" />


### Demo2: Basic 4-arm wireframe origami
The 4-arm wireframe structure is illustrated below (also see 4_arm.png). If no linkers are not provided and two staple framgents are connected by a 'TT' linker, the 3-arm wireframe structure degenerates to a 4-arm wireframe structure. 4-arm structure also doesn't have edge staples.

Linux or MacOS or Windows (powershell/cygWin)

    python ./3arm_staples.py --outdir ./ --deletion ./ToDel.txt --outname 4arm_staple_sequence

Windows (cmd)

    python .\3arm_staples.py --outdir .\ --deletion .\ToDel.txt --outname 4arm_staple_sequence

<img src="https://github.com/yanj14/Hybrid-Wireframe/blob/master/3_arm/4_arm.png" width="650" height="650" />
