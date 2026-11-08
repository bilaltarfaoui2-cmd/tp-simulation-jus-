#debit massique de départ 
m0=1000
#fraction de la m insoluble 
x0=0.02 
#fraction de la m soluble
y0=0.1 
#fraction de l'eau 
xeau=0.88
#opération unitaire 1 : filtration (m1 débit total aprés filtration )
m1=m0-(m0*x0)
print("le débit aprés filtration c'est:",m1)
#fraction de soluble aprés filtration 
y1=(m0*y0)/m1
print("fraction de soluble aprés filtration c'est:",y1)
#opération 3 ;=: chauffage
cp=3.8
q3=m1*cp
