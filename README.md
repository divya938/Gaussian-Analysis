# Gaussian-Analysis
Using this python code one can extract the trajectory of optimized strucutures from the gaussian output file, and also the energy as a function of dihedral angle?



One has to change the piece of the code according to the dihedral are scanning. In present code, the atoms contributing the dihedral are (6,1,8,9) and one can identify the value of the dihedral at a given stationary point using the string "! D*   D(6,1,8,9) ", Where * represent the dihedral number coming from your Z-matrix.


The .xvg will be the output. The energies are given in kcal/mol and the minumum energy value is shifted to 0.0 kcal/mol.
