#!/usr/bin/env python
#
# Obtain the all Cartesian coordinates of a Gaussian output file as a trajectory
#

# Load sys to additional input in the line
import sys, os

# Set global variables
start = []
end = []
elements = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fe", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Uut", "Fl", "Uup", "Lv", "Uus", "Uuo"]

# Receive the Gaussian input file
filename = sys.argv[1]

# cut extension and add xyz
xyzfile = os.path.splitext(filename)[0] + ".xyz"
energyfile = os.path.splitext(filename)[0] + ".xvg"

# Open the original file in read mode
openlog = open(filename,"r")

# Create a new file with writing rights
# overwrites old file!!
opennew = open(xyzfile,"w")
energyfileopen = open(energyfile,"w")

# Read the entire original file
rline = openlog.readlines()


# Identifyting the string
for i in range(len(rline)):
    if "Initial Parameters" in rline[i]:
       break
for j in range(i,len(rline)):
    if " Scan " in rline[j]:
       string=rline[j].split()
       break

string_to_search=string[2]
print("Dihedral",string_to_search)

# Extracting line number to get optimized structures
for i in range(len(rline)):
    if "-- Stationary point found." in rline[i]:
        for j in range(i,0,-1):
            if "Standard orientation:" in rline[j]:
                start.append(j)
                break
        for m in range (start[-1] + 5, len(rline)):
            if "---" in rline[m]:
                end.append(m)
                break
#print("Standard orientation:",start)


# Convert to formatted Cartesian coordinates
for i,iStart in enumerate(start):
   nAtoms = end[i] - (start[i]+5)
   opennew.write(str(nAtoms))
   opennew.write("\nDihedral Scan Run:\n")
   #opennew.write('\n\n')
   for line in rline[start[i]+5 : end[i]] :
      words = line.split()
      word1 = elements[int(words[1])]
      opennew.write("{:10}  {:}\n".format(word1,line[30:-1]))


Energy_line = []
Dihedral_line = []
# Extracting energies from log file
for i in range(0,len(rline)-1):
    if "-- Stationary point found." in rline[i]:
        for j in range(i,0,-1):
            if "SCF Done: " in rline[j]:
                Energy_line.append(j)
                break
        for j in range(i,len(rline)-1):
#            if "! D9    D(2,1,9,10) " in rline[j]:
            if string_to_search in rline[j]:
                Dihedral_line.append(j)
                break

# Convert to Energy of the Dihedral scan runs
energyfileopen.write(' @ title "Dihedral Scan run" \n ')
energyfileopen.write(' @ subtitle " M06-2x/6-311+g(d,p)" \n ')
energyfileopen.write(' @ xaxis label "Dihedral Angle (\c0\C)" \n ')
energyfileopen.write(' @ yaxis label "Energy (kcal/mol)" \n ')
energyfileopen.write(' @ TYPE xy \n ')
energyfileopen.write(' @ view 0.15, 0.15, 1.00, 0.85 \n ')
energyfileopen.write(' @ legend on \n ')
energyfileopen.write(' @ legend box on \n ')
energyfileopen.write(' @ legend loctype view \n ')
energyfileopen.write(' @ legend 0.78, 0.8 \n ')
energyfileopen.write(' @ legend length 2 \n ')

energy_value = []
dihedral_value = []

for i in range(len(Energy_line)) :
   line = rline[Energy_line[i]]
   energy = line.split()
   energy_value.append(energy[4])
   line = rline[Dihedral_line[i]] 
   dihedral = line.split()
   dihedral_value.append(dihedral[3])

# convertion from Hartree to kcal/mol

energy_value = [float(x)* 627.509 for x in energy_value]
min_energy_value = min(energy_value)
energy_value = [x - min_energy_value for x in energy_value]

for i in range(len(Energy_line)) :
   energyfileopen.write("{1:8.2f}  {0:10.6f}\n".format(energy_value[i],float(dihedral_value[i])))


openlog.close()
energyfileopen.close()
opennew.close()
