#This script generates oligos for 3-arm wireframe origami
import argparse
import os
import platform
import copy

# Output capitalized sequence
def path_separator():
    system=platform.system()
    path_separator=''
    if system=='Windows':
        path_separator='\\'
    else:
        path_separator='/'
    return path_separator

# Remove all the end path separators in a given string 
def remove_end_separater(in_path):
    temp_path=in_path
    while(temp_path[-1]=='\\' or temp_path[-1]=='/'):
        temp_path=temp_path[:-1]

    return temp_path
    
# Return the reverse complement 5'->3'    
def reverse_complement(input_seq):
    complementary={'a':'t', 'A':'T', 't':'a', 'T':'A', 'c':'g', 'C':'G', 'g':'c', 'G':'C'}
    output_seq=''
    for each in input_seq:
        output_seq=output_seq+complementary[each]
    return output_seq[::-1]  # Return the inverse sequence 5'->3'

# Generate the coordinate of each part of staples
def StapleCoordinate():
    p8064='ttaatttatcagctagaacggttgaatatcatattgatggtgatttgactgtctccggcctttctcacccttttgaatctttacctacacattactcaggcattgcatttaaaatatatgagggttctaaaaatttttatccttgcgttgaaataaaggcttctcccgcaaaagtattacagggtcataatgtttttggtacaaccgatttagctttatgctctgaggctttattgcttaattttgctaattctttgccttgcctgtatgatttattggatgttaatgctactactattagtagaattgatgccaccttttcagctcgcgccccaaatgaaaatatagctaaacaggttattgaccatttgcgaaatgtatctaatggtcaaactaaatctactcgttcgcagaattgggaatcaactgttatatggaatgaaacttccagacaccgtactttagttgcatatttaaaacatgttgagctacagcattatattcagcaattaagctctaagccatccgcaaaaatgacctcttatcaaaaggagcaattaaaggtactctctaatcctgacctgttggagtttgcttccggtctggttcgctttgaagctcgaattaaaacgcgatatttgaagtctttcgggcttcctcttaatctttttgatgcaatccgctttgcttctgactataatagtcagggtaaagacctgatttttgatttatggtcattctcgttttctgaactgtttaaagcatttgagggggattcaatgaatatttatgacgattccgcagtattggacgctatccagtctaaacattttactattaccccctctggcaaaacttcttttgcaaaagcctctcgctattttggtttttatcgtcgtctggtaaacgagggttatgatagtgttgctcttactatgcctcgtaattccttttggcgttatgtatctgcattagttgaatgtggtattcctaaatctcaactgatgaatctttctacctgtaataatgttgttccgttagttcgttttattaacgtagatttttcttcccaacgtcctgactggtataatgagccagttcttaaaatcgcataaggtaattcacaatgattaaagttgaaattaaaccatctcaagcccaatttactactcgttctggtgtttctcgtcagggcaagccttattcactgaatgagcagctttgttacgttgatttgggtaatgaatatccggttcttgtcaagattactcttgatgaaggtcagccagcctatgcgcctggtctgtacaccgttcatctgtcctctttcaaagttggtcagttcggttcccttatgattgaccgtctgcgcctcgttccggctaagtaacatggagcaggtcgcggatttcgacacaatttatcaggcgatgatacaaatctccgttgtactttgtttcgcgcttggtataatcgctgggggtcaaagatgagtgttttagtgtattcttttgcctctttcgttttaggttggtgccttcgtagtggcattacgtattttacccgtttaatggaaacttcctcatgaaaaagtctttagtcctcaaagcctctgtagccgttgctaccctcgttccgatgctgtctttcgctgctgagggtgacgatcccgcaaaagcggcctttaactccctgcaagcctcagcgaccgaatatatcggttatgcgtgggcgatggttgttgtcattgtcggcgcaactatcggtatcaagctgtttaagaaattcacctcgaaagcaagctgataaaccgatacaattaaaggctccttttggagccttttttttggagattttcaacgtgaaaaaattattattcgcaattcctttagttgttcctttctattctcactccgctgaaactgttgaaagttgtttagcaaaatcccatacagaaaattcatttactaacgtctggaaagacgacaaaactttagatcgttacgctaactatgagggctgtctgtggaatgctacaggcgttgtagtttgtactggtgacgaaactcagtgttacggtacatgggttcctattgggcttgctatccctgaaaatgagggtggtggctctgagggtggcggttctgagggtggcggttctgagggtggcggtactaaacctcctgagtacggtgatacacctattccgggctatacttatatcaaccctctcgacggcacttatccgcctggtactgagcaaaaccccgctaatcctaatccttctcttgaggagtctcagcctcttaatactttcatgtttcagaataataggttccgaaataggcagggggcattaactgtttatacgggcactgttactcaaggcactgaccccgttaaaacttattaccagtacactcctgtatcatcaaaagccatgtatgacgcttactggaacggtaaattcagagactgcgctttccattctggctttaatgaggatttatttgtttgtgaatatcaaggccaatcgtctgacctgcctcaacctcctgtcaatgctggcggcggctctggtggtggttctggtggcggctctgagggtggtggctctgagggtggcggttctgagggtggcggctctgagggaggcggttccggtggtggctctggttccggtgattttgattatgaaaagatggcaaacgctaataagggggctatgaccgaaaatgccgatgaaaacgcgctacagtctgacgctaaaggcaaacttgattctgtcgctactgattacggtgctgctatcgatggtttcattggtgacgtttccggccttgctaatggtaatggtgctactggtgattttgctggctctaattcccaaatggctcaagtcggtgacggtgataattcacctttaatgaataatttccgtcaatatttaccttccctccctcaatcggttgaatgtcgcccttttgtctttggcgctggtaaaccatatgaattttctattgattgtgacaaaataaacttattccgtggtgtctttgcgtttcttttatatgttgccacctttatgtatgtattttctacgtttgctaacatactgcgtaataaggagtcttaatcatgccagttcttttgggtattccgttattattgcgtttcctcggtttccttctggtaactttgttcggctatctgcttacttttcttaaaaagggcttcggtaagatagctattgctatttcattgtttcttgctcttattattgggcttaactcaattcttgtgggttatctctctgatattagcgctcaattaccctctgactttgttcagggtgttcagttaattctcccgtctaatgcgcttccctgtttttatgttattctctctgtaaaggctgctattttcatttttgacgttaaacaaaaaatcgtttcttatttggattgggataaataatatggctgtttattttgtaactggcaaattaggctctggaaagacgctcgttagcgttggtaagattcaggataaaattgtagctgggtgcaaaatagcaactaatcttgatttaaggcttcaaaacctcccgcaagtcgggaggttcgctaaaacgcctcgcgttcttagaataccggataagccttctatatctgatttgcttgctattgggcgcggtaatgattcctacgatgaaaataaaaacggcttgcttgttctcgatgagtgcggtacttggtttaatacccgttcttggaatgataaggaaagacagccgattattgattggtttctacatgctcgtaaattaggatgggatattatttttcttgttcaggacttatctattgttgataaacaggcgcgttctgcattagctgaacatgttgtttattgtcgtcgtctggacagaattactttaccttttgtcggtactttatattctcttattactggctcgaaaatgcctctgcctaaattacatgttggcgttgttaaatatggcgattctcaattaagccctactgttgagcgttggctttatactggtaagaatttgtataacgcatatgatactaaacaggctttttctagtaattatgattccggtgtttattcttatttaacgccttatttatcacacggtcggtatttcaaaccattaaatttaggtcagaagatgaaattaactaaaatatatttgaaaaagttttctcgcgttctttgtcttgcgattggatttgcatcagcatttacatatagttatataacccaacctaagccggaggttaaaaaggtagtctctcagacctatgattttgataaattcactattgactcttctcagcgtcttaatctaagctatcgctatgttttcaaggattctaagggaaaattaattaatagcgacgatttacagaagcaaggttattcactcacatatattgatttatgtactgtttccattaaaaaaggtaattcaaatgaaattgttaaatgtaattaattttgttttcttgatgtttgtttcatcatcttcttttgctcaggtaattgaaatgaataattcgcctctgcgcgattttgtaacttggtattcaaagcaatcaggcgaatccgttattgtttctcccgatgtaaaaggtactgttactgtatattcatctgacgttaaacctgaaaatctacgcaatttctttatttctgttttacgtgcaaataattttgatatggtaggttctaacccttccattattcagaagtataatccaaacaatcaggattatattgatgaattgccatcatctgataatcaggaatatgatgataattccgctccttctggtggtttctttgttccgcaaaatgataatgttactcaaacttttaaaattaataacgttcgggcaaaggatttaatacgagttgtcgaattgtttgtaaagtctaatacttctaaatcctcaaatgtattatctattgacggctctaatctattagttgttagtgctcctaaagatattttagataaccttcctcaattcctttcaactgttgatttgccaactgaccagatattgattgagggtttgatatttgaggttcagcaaggtgatgctttagatttttcatttgctgctggctctcagcgtggcactgttgcaggcggtgttaatactgaccgcctcacctctgttttatcttctgctggtggttcgttcggtatttttaatggcgatgttttagggctatcagttcgcgcattaaagactaatagccattcaaaaatattgtctgtgccacgtattcttacgctttcaggtcagaagggttctatctctgttggccagaatgtcccttttattactggtcgtgtgactggtgaatctgccaatgtaaataatccatttcagacgattgagcgtcaaaatgtaggtatttccatgagcgtttttcctgttgcaatggctggcggtaatattgttctggatattaccagcaaggccgatagtttgagttcttctactcaggcaagtgatgttattactaatcaaagaagtattgctacaacggttaatttgcgtgatggacagactcttttactcggtggcctcactgattataaaaacacttctcaggattctggcgtaccgttcctgtctaaaatccctttaatcggcctcctgtttagctcccgctctgattctaacgaggaaagcacgttatacgtgctcgtcaaagcaaccatagtacgcgccctgtagcggcgcattaagcgcggcgggtgtggtggttacgcgcagcgtgaccgctacacttgccagcgccctagcgcccgctcctttcgctttcttcccttcctttctcgccacgttcgccggctttccccgtcaagctctaaatcgggggctccctttagggttccgatttagtgctttacggcacctcgaccccaaaaaacttgatttgggtgatggttcacgtagtgggccatcgccctgatagacggtttttcgccctttgacgttggagtccacgttctttaatagtggactcttgttccaaactggaacaacactcaaccctatctcgggctattcttttgatttataagggattttgccgatttcggaaccaccatcaaacaggattttcgcctgctggggcaaaccagcgtggaccgcttgctgcaactctctcagggccaggcggtgaagggcaatcagctgttgcccgtctcactggtgaaaagaaaaaccaccctggcgcccaatacgcaaaccgcctctccccgcgcgttggccgattcattaatgcagctggcacgacaggtttcccgactggaaagcgggcagtgagcgcaacgcaattaatgtgagttagctcactcattaggcaccccaggctttacactttatgcttccggctcgtatgttgtgtggaattgtgagcggataacaatttcacacaggaaacagctatgaccatgattacgaattcgagctcggtacccggggatcctcaactgtgaggaggctcacggacgcgaagaacaggcacgcgtgctggcagaaacccccggtatgaccgtgaaaacggcccgccgcattctggccgcagcaccacagagtgcacaggcgcgcagtgacactgcgctggatcgtctgatgcagggggcaccggcaccgctggctgcaggtaacccggcatctgatgccgttaacgatttgctgaacacaccagtgtaagggatgtttatgacgagcaaagaaacctttacccattaccagccgcagggcaacagtgacccggctcataccgcaaccgcgcccggcggattgagtgcgaaagcgcctgcaatgaccccgctgatgctggacacctccagccgtaagctggttgcgtgggatggcaccaccgacggtgctgccgttggcattcttgcggttgctgctgaccagaccagcaccacgctgacgttctacaagtccggcacgttccgttatgaggatgtgctctggccggaggctgccagcgacgagacgaaaaaacggaccgcgtttgccggaacggcaatcagcatcgtttaactttacccttcatcactaaaggccgcctgtgcggctttttttacgggatttttttatgtcgatgtacacaaccgcccaactgctggcggcaaatgagcagaaatttaagtttgatccgctgtttctgcgtctctttttccgtgagagctatcccttcaccacggagaaagtctatctctcacaaattccgggactggtaaacatggcgctgtacgtttcgccgattgtttccggtgaggttatccgttcccgtggcggctccacctctgaaagcttggcactggccgtcgttttacaacgtcgtgactgggaaaaccctggcgttacccaacttaatcgccttgcagcacatccccctttcgccagctggcgtaatagcgaagaggcccgcaccgatcgcccttcccaacagttgcgcagcctgaatggcgaatggcgctttgcctggtttccggcaccagaagcggtgccggaaagctggctggagtgcgatcttcctgaggccgatactgtcgtcgtcccctcaaactggcagatgcacggttacgatgcgcccatctacaccaacgtgacctatcccattacggtcaatccgccgtttgttcccacggagaatccgacgggttgttactcgctcacatttaatgttgatgaaagctggctacaggaaggccagacgcgaattatttttgatggcgttcctattggttaaaaaatgagctgatttaacaaaaatttaatgcgaattttaacaaaatattaacgtttacaatttaaatatttgcttatacaatcttcctgtttttggggcttttctgattatcaaccggggtacatatgattgacatgctagttttacgattaccgttcatcgattctcttgtttgctccagactctcaggcaatgacctgatagcctttgtagatctctcaaaaatagctaccctctccggca'
    # segment the p8064 into segments of 921nt, each segement has two sub-regions of 431nt. The two sub-region are separated by a 35nt region
    # Two adjacent 921 segments have 443nt overlap
    # The 3-arm wireframe has 13 segements in total.

    # Generate sequences of staple fragments
    StapleDict=dict()  # Keep sequences of whole staples 
    OligoDict=dict()   # Keep staple fragment sequences
    seg_list=[]        # keep all segments
    for i in range(13):
        seg_start=443*i+35*i  # Start of a segment
        seg_end=seg_start+921 # End of a segment, [)
        seg_list.append([seg_start, seg_end, i])  

    for i in range(13):
        # Get the first pair of staples of each segment
        first_No=i*17+1  # The number ID of the first staple of each segment
        second_No=i*17+2 # Number ID of the second
        first_5end=reverse_complement(p8064[seg_list[i][1]-11:seg_list[i][1]])
        first_3end=reverse_complement(p8064[seg_list[i][0]:seg_list[i][0]+10])
        second_3end=reverse_complement(p8064[seg_list[i][1]-26:seg_list[i][1]-13])
        second_5end=reverse_complement(p8064[seg_list[i][0]+12: seg_list[i][0]+25])
        OligoDict[first_No]=[first_5end, first_3end]
        OligoDict[second_No]=[second_5end, second_3end]

        # Generate the next seven pairs of oligos for each segment
        for j in range(7):
            first_No=(i*17+1)+((j+1)*2)
            second_No=(i*17+2)+((j+1)*2)
            pair_start=seg_list[i][0]+53+(j*56)  # The 5' of the pair on p8064
            pair_end=seg_list[i][1]-54-(j*56)    # The 3' of the pair on p8064
            first_5end=reverse_complement(p8064[pair_end-13: pair_end])
            first_3end=reverse_complement(p8064[pair_start:pair_start+13])
            second_3end=reverse_complement(p8064[pair_end-28:pair_end-15])
            second_5end=reverse_complement(p8064[pair_start+15:pair_start+28])
            OligoDict[first_No]=[first_5end, first_3end] # Two fragments of first staple in the pair
            OligoDict[second_No]=[second_5end, second_3end] # Two fragments of second staple in the pair
    
    # Genrate the edge staples
    for i in range(13):
        edge_No=(i+1)*17
        temp_seg1=reverse_complement(p8064[seg_list[i][0]+467: seg_list[i][0]+478]) #5' part of the edge staple
        temp_seg2=reverse_complement(p8064[seg_list[i][0]+455: seg_list[i][0]+465]) #middle part of the edge staple
        temp_seg3=reverse_complement(p8064[seg_list[i][0]+443: seg_list[i][0]+453]) #3' part of the edge staple
        edge_temp=temp_seg1+'TT'+temp_seg2+'TT'+temp_seg3+'\n'
        StapleDict[edge_No]=edge_temp  # Add sequence of the edge staples to the staple dict

    return OligoDict, StapleDict

# Generate complete sequences of each staple 
# Print the staples to a txt file (tab delimited). Current working directory is the default output directory
def StapleGenerator(OligoDict, StapleDict, outdir=os.getcwd(), linker='', delStaple='', outname='Staple_sequences'):
    separator=path_separator()  # Get system dependent path separator
    staple_seq=open(outdir+separator+outname+".txt", "w") 
    counter_dict=copy.deepcopy(OligoDict) # To record all staples that are not given staples

    if linker == '':
        print ("No input file specified!")
        print ("Default 'TT' will be used as the linker")
        for key, value in OligoDict.items():
            StapleDict[key]=value[0]+'TT'+value[1]+'\n'

    else:
        Input_dsRegion=open(linker, 'r')
        all_dsRegion=Input_dsRegion.readlines()  # First element is staple number id and the second element is staple linker sequence
        for eachLinker in all_dsRegion:
            each_linker=eachLinker.strip().split()
            # Proceed only when the line is not empty
            if each_linker:
                linker_number=int(each_linker[0])
                if linker_number in OligoDict:
                    temp=OligoDict[linker_number] # Get the staple fragment sequence list
                    temp_seq=temp[0]+'TT'+each_linker[1]+'TT'+temp[1]+'\n'
                    StapleDict[linker_number]=temp_seq

                del counter_dict[linker_number]         
        Input_dsRegion.close()

    # To delete staples as indicated by the 
    if  delStaple!='':
        del_staple_file=open(delStaple, 'r')
        del_staple=del_staple_file.readlines()
        for each_del in del_staple:
            del StapleDict[int(each_del.strip())]
        del_staple_file.close()

    # All staples without a provided linker will be connected by 'TT'
    if counter_dict:
        for key, value in counter_dict.items():
            StapleDict[key]= value[0]+'TT'+value[1]+'\n'  

    # Sort the dictionary by key value and print out the staple sequences
    for staple_no in sorted (StapleDict.keys()):
        staple_seq.write(str(staple_no)+'\t'+StapleDict[staple_no])


    staple_seq.close()


def main():
    parser=argparse.ArgumentParser(description='Generate a staples in a 3arm_staples.txt file')
    parser.add_argument("--outdir", default=os.getcwd(), help="Staple output directory, default is current working directory")
    parser.add_argument("--linker", default='', help="Linker file (details in the document), default is 'TT'")
    parser.add_argument("--deletion", default='', help="Path to the text file with all staples to be deleted (specified by the staple numbers)")
    parser.add_argument("--outname", default='Staple_sequences', help="The name of the output staple sequence file (no file extension should be included). Default is 'Staple_sequences'.")

    args=parser.parse_args()
    outdir=args.outdir
    linker=args.linker
    delStaple=args.deletion
    outname=args.outname

    # Just in case users add a separator at the end of file path
    # Remove the end separator if there is one
    if linker!='':
        linker=remove_end_separater(linker)
    if delStaple!='':   
        delStaple=remove_end_separater(delStaple)

    frags=StapleCoordinate() # Return a list of two dictionary, first to store staple frag seq, second to store staple seq
    OligoDict, StapleDict=frags[0], frags[1] 
    StapleGenerator(OligoDict, StapleDict, outdir, linker, delStaple, outname)

if __name__ == '__main__':
    main()