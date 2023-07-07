import re
import csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2


#____________________
# NCBI REFSEQ DATABASE

file_path = "assembly_summary.txt"  
with open(file_path, "r") as file:
    lines = file.readlines()

organism_names = []
for line in lines:
    if not line.startswith("#"):  
        columns = line.strip().split("\t")
        organism_name = columns[7]
        organism_name = re.sub(r'[^a-zA-Z0-9\s]', '', organism_name)  
        organism_name = organism_name.lower() 
        organism_names.append(organism_name)

print(len(organism_names))

#_______________________________

# ENSEMBLE DATABASE


filtered_names = []

with open('ensemble_name.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name = row[0]
        
        name_parts = name.split('_')
        filtered_name = ' '.join(name_parts[:2])
        
        filtered_names.append(filtered_name)

print(len(filtered_names))
#________________________

def compare_organism_names(database1, database2):
    complete_match = []
    one_match = []
    database1_no_match = []
    database2_no_match = []

    for name1 in database1:
        found_match = False

        for name2 in database2:
            if name1 == name2:
                complete_match.append(name1)
                found_match = True
                break

            words1 = name1.split()
            words2 = name2.split()

            if len(words1) == 2 and len(words2) == 2:
                if words1[0] == words2[0] or words1[0] == words2[1] or words1[1] == words2[0] or words1[1] == words2[1]:
                    one_match.append((name1, name2))
                    found_match = True
                    break

        if not found_match:
            database1_no_match.append(name1)

    for name2 in database2:
        if name2 not in database1:
            database2_no_match.append(name2)

    return complete_match, one_match, database1_no_match, database2_no_match

complete_match, one_match, database1_no_match, database2_no_match = compare_organism_names(organism_names, filtered_names)

print(len(complete_match))
print(len(one_match))

venn2(subsets=(len(organism_names) - len(database1_no_match),
               len(filtered_names) - len(database2_no_match),
               len(complete_match)),
      set_labels=('REFSEQ', 'ENSEMBLE'))

plt.text(-0.2, -0.1, f"Only in Database 1: {len(database1_no_match)}",
         fontsize=12, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
plt.text(1.05, -0.1, f"Only in Database 2: {len(database2_no_match)}",
         fontsize=12, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
plt.text(0.4, 0.5, f"Complete Match: {len(complete_match)}",
         fontsize=12, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
plt.text(0.55, 0.1, f"One Match: {len(one_match)}",
         fontsize=12, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

plt.tight_layout()
plt.show()
plt.savefig("two_compare.png")