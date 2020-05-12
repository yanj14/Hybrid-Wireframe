import argparse
import copy
import os
import platform

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

# Output the reverse complement 5'->3'    
def reverse_complement(input_seq):
    complementary={'a':'t', 'A':'T', 't':'a', 'T':'A', 'c':'g', 'C':'G', 'g':'c', 'G':'C'}
    output_seq=''
    for each in input_seq:
        output_seq=output_seq+complementary[each]
    return output_seq[::-1]  #return the inverse sequence 5'->3'

# Get the Coordinate (start and end) of each fragment of each staple
def get_coordinate_dict(delStaple):
    separator=path_separator()  # Get system dependent path separator
    f=open(os.getcwd()+separator+'Staples_info.txt', 'r') # Read the staple coordinate info of the 1st segment of 6-arm structure
    all_lines=f.readlines() 
    staple_list=[] # Store staple coordinate info
    staple_dict=dict() # {staple fragment name: coordinate}

    # Get staple coordinates of the first segment
    for i in range(0, len(all_lines), 2):
        temp_coordinate=all_lines[i].strip().split()[1].split('..') # Staple fragment coordinate
        temp_name=all_lines[i+1].strip().split()[0][7:] # Staple name
        staple_list.append([temp_name[-1]+temp_name[:-1], int(temp_coordinate[0])-1, int(temp_coordinate[1])]) #[)

    Total_staple_list=copy.deepcopy(staple_list)
    
    # Generate all the rest staples (1-6 segments)
    for i in range(5):
        for each_staple in staple_list:
            Total_staple_list.append([each_staple[0]+'_seg'+str(i+2), each_staple[1]-990*(i+1), each_staple[2]-990*(i+1)])

    # Convert all staples coordinate list into dictionary
    for each_staple in Total_staple_list:
        staple_dict[each_staple[0]]=[each_staple[1], each_staple[2]]

    # Remove bottom edge staples of segment 6
    for i in range(27, 38, 1):
        del staple_dict['a'+str(i)+'_seg6']
        del staple_dict['b'+str(i)+'_seg6']

    # Remove the coordinates of unwanted staples (ToDel, give by the --deletion option argument)
    if delStaple !="":
        stapleDel=open(delStaple, 'r').readlines()
        for eachDel in stapleDel:
            temp_a='a'+eachDel.strip()
            temp_b='b'+eachDel.strip()
            if temp_a in staple_dict and temp_b in staple_dict:
                del staple_dict[temp_a]
                del staple_dict[temp_b]
            else:
                continue

    f.close()
    return staple_dict

#The linker file should be a tab delimited txt file
#first part of staple (name)+'\t'+second part of staple (name)+'\t'+linker(sequence)+'\t\+'start/end+'\n'
def staple_generator(staple_dict, outdir=os.getcwd(), linker='',dsOption=False):
    p8064='tatttttgagagatctacaaaggctatcaggtcattgcctgagagtctggagcaaacaagagaatcgatgaacggtaatcgtaaaactagcatgtcaatcatatgtaccccggttgataatcagaaaagccccaaaaacaggaagattgtataagcaaatatttaaattgtaaacgttaatattttgttaaaattcgcattaaatttttgttaaatcagctcattttttaaccaataggaacgccatcaaaaataattcgcgtctggccttcctgtagccagctttcatcaacattaaatgtgagcgagtaacaacccgtcggattctccgtgggaacaaacggcggattgaccgtaatgggataggtcacgttggtgtagatgggcgcatcgtaaccgtgcatctgccagtttgaggggacgacgacagtatcggcctcaggaagatcgcactccagccagctttccggcaccgcttctggtgccggaaaccaggcaaagcgccattcgccattcaggctgcgcaactgttgggaagggcgatcggtgcgggcctcttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaacgccagggttttcccagtcacgacgttgtaaaacgacggccagtgccaagctttcagaggtggagccgccacgggaacggataacctcaccggaaacaatcggcgaaacgtacagcgccatgtttaccagtcccggaatttgtgagagatagactttctccgtggtgaagggatagctctcacggaaaaagagacgcagaaacagcggatcaaacttaaatttctgctcatttgccgccagcagttgggcggttgtgtacatcgacataaaaaaatcccgtaaaaaaagccgcacaggcggcctttagtgatgaagggtaaagttaaacgatgctgattgccgttccggcaaacgcggtccgttttttcgtctcgtcgctggcagcctccggccagagcacatcctcataacggaacgtgccggacttgtagaacgtcagcgtggtgctggtctggtcagcagcaaccgcaagaatgccaacggcagcaccgtcggtggtgccatcccacgcaaccagcttacggctggaggtgtccagcatcagcggggtcattgcaggcgctttcgcactcaatccgccgggcgcggttgcggtatgagccgggtcactgttgccctgcggctggtaatgggtaaaggtttctttgctcgtcataaacatcccttacactggtgtgttcagcaaatcgttaacggcatcagatgccgggttacctgcagccagcggtgccggtgccccctgcatcagacgatccagcgcagtgtcactgcgcgcctgtgcactctgtggtgctgcggccagaatgcggcgggccgttttcacggtcataccgggggtttctgccagcacgcgtgcctgttcttcgcgtccgtgagcctcctcacagttgaggatccccgggtaccgagctcgaattcgtaatcatggtcatagctgtttcctgtgtgaaattgttatccgctcacaattccacacaacatacgagccggaagcataaagtgtaaagcctggggtgcctaatgagtgagctaactcacattaattgcgttgcgctcactgcccgctttccagtcgggaaacctgtcgtgccagctgcattaatgaatcggccaacgcgcggggagaggcggtttgcgtattgggcgccagggtggtttttcttttcaccagtgagacgggcaacagctgattgcccttcaccgcctggccctgagagagttgcagcaagcggtccacgctggtttgccccagcaggcgaaaatcctgtttgatggtggttccgaaatcggcaaaatcccttataaatcaaaagaatagcccgagatagggttgagtgttgttccagtttggaacaagagtccactattaaagaacgtggactccaacgtcaaagggcgaaaaaccgtctatcagggcgatggcccactacgtgaaccatcacccaaatcaagttttttggggtcgaggtgccgtaaagcactaaatcggaaccctaaagggagcccccgatttagagcttgacggggaaagccggcgaacgtggcgagaaaggaagggaagaaagcgaaaggagcgggcgctagggcgctggcaagtgtagcggtcacgctgcgcgtaaccaccacacccgccgcgcttaatgcgccgctacagggcgcgtactatggttgctttgacgagcacgtataacgtgctttcctcgttagaatcagagcgggagctaaacaggaggccgattaaagggattttagacaggaacggtacgccagaatcctgagaagtgtttttataatcagtgaggccaccgagtaaaagagtctgtccatcacgcaaattaaccgttgtagcaatacttctttgattagtaataacatcacttgcctgagtagaagaactcaaactatcggccttgctggtaatatccagaacaatattaccgccagccattgcaacaggaaaaacgctcatggaaatacctacattttgacgctcaatcgtctgaaatggattatttacattggcagattcaccagtcacacgaccagtaataaaagggacattctggccaacagagatagaacccttctgacctgaaagcgtaagaatacgtggcacagacaatatttttgaatggctattagtctttaatgcgcgaactgatagccctaaaacatcgccattaaaaataccgaacgaaccaccagcagaagataaaacagaggtgaggcggtcagtattaacaccgcctgcaacagtgccacgctgagagccagcagcaaatgaaaaatctaaagcatcaccttgctgaacctcaaatatcaaaccctcaatcaatatctggtcagttggcaaatcaacagttgaaaggaattgaggaaggttatctaaaatatctttaggagcactaacaactaatagattagagccgtcaatagataatacatttgaggatttagaagtattagactttacaaacaattcgacaactcgtattaaatcctttgcccgaacgttattaattttaaaagtttgagtaacattatcattttgcggaacaaagaaaccaccagaaggagcggaattatcatcatattcctgattatcagatgatggcaattcatcaatataatcctgattgtttggattatacttctgaataatggaagggttagaacctaccatatcaaaattatttgcacgtaaaacagaaataaagaaattgcgtagattttcaggtttaacgtcagatgaatatacagtaacagtaccttttacatcgggagaaacaataacggattcgcctgattgctttgaataccaagttacaaaatcgcgcagaggcgaattattcatttcaattacctgagcaaaagaagatgatgaaacaaacatcaagaaaacaaaattaattacatttaacaatttcatttgaattaccttttttaatggaaacagtacataaatcaatatatgtgagtgaataaccttgcttctgtaaatcgtcgctattaattaattttcccttagaatccttgaaaacatagcgatagcttagattaagacgctgagaagagtcaatagtgaatttatcaaaatcataggtctgagagactacctttttaacctccggcttaggttgggttatataactatatgtaaatgctgatgcaaatccaatcgcaagacaaagaacgcgagaaaactttttcaaatatattttagttaatttcatcttctgacctaaatttaatggtttgaaataccgaccgtgtgataaataaggcgttaaataagaataaacaccggaatcataattactagaaaaagcctgtttagtatcatatgcgttatacaaattcttaccagtataaagccaacgctcaacagtagggcttaattgagaatcgccatatttaacaacgccaacatgtaatttaggcagaggcattttcgagccagtaataagagaatataaagtaccgacaaaaggtaaagtaattctgtccagacgacgacaataaacaacatgttcagctaatgcagaacgcgcctgtttatcaacaatagataagtcctgaacaagaaaaataatatcccatcctaatttacgagcatgtagaaaccaatcaataatcggctgtctttccttatcattccaagaacgggtattaaaccaagtaccgcactcatcgagaacaagcaagccgtttttattttcatcgtaggaatcattaccgcgcccaatagcaagcaaatcagatatagaaggcttatccggtattctaagaacgcgaggcgttttagcgaacctcccgacttgcgggaggttttgaagccttaaatcaagattagttgctattttgcacccagctacaattttatcctgaatcttaccaacgctaacgagcgtctttccagagcctaatttgccagttacaaaataaacagccatattatttatcccaatccaaataagaaacgattttttgtttaacgtcaaaaatgaaaatagcagcctttacagagagaataacataaaaacagggaagcgcattagacgggagaattaactgaacaccctgaacaaagtcagagggtaattgagcgctaatatcagagagataacccacaagaattgagttaagcccaataataagagcaagaaacaatgaaatagcaatagctatcttaccgaagccctttttaagaaaagtaagcagatagccgaacaaagttaccagaaggaaaccgaggaaacgcaataataacggaatacccaaaagaactggcatgattaagactccttattacgcagtatgttagcaaacgtagaaaatacatacataaaggtggcaacatataaaagaaacgcaaagacaccacggaataagtttattttgtcacaatcaatagaaaattcatatggtttaccagcgccaaagacaaaagggcgacattcaaccgattgagggagggaaggtaaatattgacggaaattattcattaaaggtgaattatcaccgtcaccgacttgagccatttgggaattagagccagcaaaatcaccagtagcaccattaccattagcaaggccggaaacgtcaccaatgaaaccatcgatagcagcaccgtaatcagtagcgacagaatcaagtttgcctttagcgtcagactgtagcgcgttttcatcggcattttcggtcatagcccccttattagcgtttgccatcttttcataatcaaaatcaccggaaccagagccaccaccggaaccgcctccctcagagccgccaccctcagaaccgccaccctcagagccaccaccctcagagccgccaccagaaccaccaccagagccgccgccagcattgacaggaggttgaggcaggtcagacgattggccttgatattcacaaacaaataaatcctcattaaagccagaatggaaagcgcagtctctgaatttaccgttccagtaagcgtcatacatggcttttgatgatacaggagtgtactggtaataagttttaacggggtcagtgccttgagtaacagtgcccgtataaacagttaatgccccctgcctatttcggaacctattattctgaaacatgaaagtattaagaggctgagactcctcaagagaaggattaggattagcggggttttgctcagtaccaggcggataagtgccgtcgagagggttgatataagtatagcccggaataggtgtatcaccgtactcaggaggtttagtaccgccaccctcagaaccgccaccctcagaaccgccaccctcagagccaccaccctcattttcagggatagcaagcccaataggaacccatgtaccgtaacactgagtttcgtcaccagtacaaactacaacgcctgtagcattccacagacagccctcatagttagcgtaacgatctaaagttttgtcgtctttccagacgttagtaaatgaattttctgtatgggattttgctaaacaactttcaacagtttcagcggagtgagaatagaaaggaacaactaaaggaattgcgaataataattttttcacgttgaaaatctccaaaaaaaaggctccaaaaggagcctttaattgtatcggtttatcagcttgctttcgaggtgaatttcttaaacagcttgataccgatagttgcgccgacaatgacaacaaccatcgcccacgcataaccgatatattcggtcgctgaggcttgcagggagttaaaggccgcttttgcgggatcgtcaccctcagcagcgaaagacagcatcggaacgagggtagcaacggctacagaggctttgaggactaaagactttttcatgaggaagtttccattaaacgggtaaaatacgtaatgccactacgaaggcaccaacctaaaacgaaagaggcaaaagaatacactaaaacactcatctttgacccccagcgattataccaagcgcgaaacaaagtacaacggagatttgtatcatcgcctgataaattgtgtcgaaatccgcgacctgctccatgttacttagccggaacgaggcgcagacggtcaatcataagggaaccgaactgaccaactttgaaagaggacagatgaacggtgtacagaccaggcgcataggctggctgaccttcatcaagagtaatcttgacaagaaccggatattcattacccaaatcaacgtaacaaagctgctcattcagtgaataaggcttgccctgacgagaaacaccagaacgagtagtaaattgggcttgagatggtttaatttcaactttaatcattgtgaattaccttatgcgattttaagaactggctcattataccagtcaggacgttgggaagaaaaatctacgttaataaaacgaactaacggaacaacattattacaggtagaaagattcatcagttgagatttaggaataccacattcaactaatgcagatacataacgccaaaaggaattacgaggcatagtaagagcaacactatcataaccctcgtttaccagacgacgataaaaaccaaaatagcgagaggcttttgcaaaagaagttttgccagagggggtaatagtaaaatgtttagactggatagcgtccaatactgcggaatcgtcataaatattcattgaatccccctcaaatgctttaaacagttcagaaaacgagaatgaccataaatcaaaaatcaggtctttaccctgactattatagtcagaagcaaagcggattgcatcaaaaagattaagaggaagcccgaaagacttcaaatatcgcgttttaattcgagcttcaaagcgaaccagaccggaagcaaactccaacaggtcaggattagagagtacctttaattgctccttttgataagaggtcatttttgcggatggcttagagcttaattgctgaatataatgctgtagctcaacatgttttaaatatgcaactaaagtacggtgtctggaagtttcattccatataacagttgattcccaattctgcgaacgagtagatttagtttgaccattagatacatttcgcaaatggtcaataacctgtttagctatattttcatttggggcgcgagctgaaaaggtggcatcaattctactaatagtagtagcattaacatccaataaatcatacaggcaaggcaaagaattagcaaaattaagcaataaagcctcagagcataaagctaaatcggttgtaccaaaaacattatgaccctgtaatacttttgcgggagaagcctttatttcaacgcaaggataaaaatttttagaaccctcatatattttaaatgcaatgcctgagtaatgtgtaggtaaagattcaaaagggtgagaaaggccggagacagtcaaatcaccatcaatatgatattcaaccgttctagctgataaattaatgccggagagggtagc'
    separator=path_separator()  # Get system dependent path separator
    if linker=='':
        temp_file=open(outdir+separator+'6arm_staples.txt', 'w') # Write staple sequences
        print ("No linker file input!")
        print ("Use 'TT' as the linker between two fragments of staples")
        staples=[]
        for key, value in staple_dict.items():
            staples.append([key, value[0], value[1]])
        staples.sort()  #Order the list by strand a (first half) and strand b (second half) while the name for the oligos is the same for strand a and b
        temp_len=int(len(staples)/2)
        for i in range(temp_len):
            temp_file.write(staples[i][0][1:] +'\t'+ p8064[staples[i][1]:staples[i][2]]+'TT'+p8064[staples[i+temp_len][1]:staples[i+temp_len][2]] +'\n')
        temp_file.close()
    
    else:
        counter_dict=copy.deepcopy(staple_dict) #Copy the staple_dict to record which staples aren't provided with linker sequences
        temp_file=open(outdir+separator+'6arm_staples.txt', 'w') # Write staple sequences
        input_linkers=open(linker, 'r') # Linker sequence file
        all_linkers=input_linkers.readlines()
        for each_linker in all_linkers:
            # Filter all empty lines in the linker seq file
            if each_linker.strip() != '':
                tempLinkerInfo=each_linker.strip().split('\t') #frag a, frag b, seq
                frag_first=staple_dict[tempLinkerInfo[0]] #frag_first is a list [start, end]
                frag_second=staple_dict[tempLinkerInfo[1]] #frag_second is a list [start, end]
                
                # Remove the staple frags that are provided with the linkers
                del counter_dict[tempLinkerInfo[0]] 
                del counter_dict[tempLinkerInfo[1]]
                
                # Insert ssDNA linkers or dsDNA linkers
                if dsOption==False:
                    temp_file.write(tempLinkerInfo[0][1:] +'\t'+ p8064[frag_first[0]:frag_first[1]]+'TT'+tempLinkerInfo[2]+'TT'+p8064[frag_second[0]: frag_second[1]] +'\n')
                else:
                    if tempLinkerInfo[3]=='start':
                        temp_file.write(tempLinkerInfo[0] +'\t'+ tempLinkerInfo[2]+'TT'+p8064[frag_first[0]:frag_first[1]] +'\n')
                        temp_file.write(tempLinkerInfo[1] +'\t'+ reverse_complement(tempLinkerInfo[2])+'TT'+p8064[frag_second[0]:frag_second[1]] +'\n')
                    else:    
                        temp_file.write(tempLinkerInfo[0] +'\t'+ p8064[frag_first[0]:frag_first[1]]+'TT'+tempLinkerInfo[2] +'\n')
                        temp_file.write(tempLinkerInfo[1] +'\t'+ p8064[frag_second[0]:frag_second[1]]+'TT'+reverse_complement(tempLinkerInfo[2]) +'\n')
        
        # Fragments without provided linkers will be connected by a 'TT' linker
        staples=[]
        for key, value in counter_dict.items():
            staples.append([key, value[0], value[1]])
        staples.sort()  #Order the list by strand a (first half) and strand b (second half) while the name for the oligos is the same for strand a and b
        temp_len=int(len(staples)/2)
        for i in range(temp_len):
            temp_file.write(staples[i][0][1:] +'\t'+ p8064[staples[i][1]:staples[i][2]]+'TT'+p8064[staples[i+temp_len][1]:staples[i+temp_len][2]] +'\n')            
            
        temp_file.close()
            
def main():
    parser=argparse.ArgumentParser(description='Generate a staples in a 6arm_staples.txt file')
    parser.add_argument("--outdir", default=os.getcwd(), help="Staple output directory, default is current working directory")
    parser.add_argument("--linker", default='', help="linker file (details in the document), default is 'TT'")
    parser.add_argument("--deletion", default='', help="Path to the text file with all staples to be deleted (specified by the staple numbers)")
    parser.add_argument("--dsOption", default='0', help="1 (linker is dsDNA) or 0 (linker is ssDNA), default is 0")

    args=parser.parse_args()
    outdir=args.outdir
    linker=args.linker
    delStaple=args.deletion
    dsOption=int(args.dsOption)

    # Just in case users add a separator at the end of file path
    # Remove the end separator if there is one
    if linker!='':
        linker=remove_end_separater(linker)
    if delStaple!='':   
        delStaple=remove_end_separater(delStaple)

    temp_dict=get_coordinate_dict(delStaple) # Get coordinate info
    staple_generator(temp_dict, outdir, linker,dsOption) # Generate staples

if __name__ == '__main__':
    main()