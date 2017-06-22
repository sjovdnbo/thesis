import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
def mergedata(yearsptr,numbersptr):
    data = []

    for i in range(len(yearsptr)):
        for j in range(numbersptr[i]):
            data.append(yearsptr[i])
    return data
numberptr = np.array([99, 77, 70, 80, 55, 49, 28, 37, 32, 22, 24, 25, 12, 12, 14, 18, 6, 4, 4, 3, 5, 3, 6, 6, 3, 2, 3, 2, 0, 1, 8, 0, 2, 1, 3, 1, 2, 0, 2, 1, 0, 1, 0, 2, 1, 0, 0, 0, 3, 2, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0][::-1])
numberdia = np.array([199,224,203,169,144,143,103,115,116,81,74,70,48,41,36,25,28,18,12,20,9,8,15,5,2,3,3,3,1,1,2,3,2,0,1,2,3,1,4,1,1,0,1,1,1,0,3,1,4,2,4,0,0,1,2,0,0,0,1,0,0,0,0,0,0,0,0][::-1])
yearsptr = np.array(range(1950, 2017))
sns.set_style("white")
f,(ax1,ax2)= plt.subplots(nrows=1,ncols=2)

hist1 = sns.distplot(np.array(mergedata(yearsptr=yearsptr, numbersptr=numberdia)), kde=False, ax=ax1)
hist1.set(xlabel="year", ylabel="number of publications")
hist1.set(xlim=(1950, 2017))
hist1.set_title("Publications on marine diatoms")

hist2 = sns.distplot(np.array(mergedata(yearsptr=yearsptr,numbersptr=numberptr)), kde=False,ax=ax2)
hist2.set(xlabel = "year",ylabel = "number of publications")
hist2.set(xlim=(1950,2017))
hist2.set_title("Publications on Phaeodactylum tricornutum")
f.tight_layout()

f.savefig("C:/Users/beheerder/Google Drive/univ/bioinformatics 2/thesis/figures/diatomspublications.png", dpi=500)
plt.show()


