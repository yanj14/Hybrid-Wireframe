# **Hybrid wireframe origami**

Here we deposit two scripts to generate hybrid wireframe origami structures. We designed the basic 3-arm, 4-arm and 6-arm structures. **M13 p8064 ssDNA** was the scaffold and **staples (short ssDNA oligos)** were used to establish the shapes and patterns.

Each staple contains several fragments (>=2) and two of them directly bind to the scaffold. To generate variants of those basic structures, the two fragments that bind directly to p8064 were not changed and between them, different linkers were inserted such as short stretch of ssDNA, dsDNA.

The two scripts here first index p8064 and obtain the coordinate/sequences of staple fragments that directly bind p8064. Then the linker sequence file that specify the connection patterns of linkers with staples is loaded and all staple sequences are ouput in a .txt file.

For more details, please refer to the Readme.md files in the 6_arm and 3_arm folders.