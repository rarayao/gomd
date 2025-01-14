#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

p = argparse.ArgumentParser()

p.add_argument("fname", type=str, help="Input file, gomd format")
p.add_argument("-c",type=int, help="Columns in the gomd files, not counting the time (i.e first) column",default=1)
p.add_argument("--tbf", type=float, help="delta time between frames, if applicable", default=1)
p.add_argument("--xlabel", type=str, help="Label for the X axis", default="Time")
tagsstring=p.add_argument("--tags", type=str, help="Tags for the Y axis and for each plotted thing,",default="")
p.add_argument("--onlyplot",type=int,help="Print only the Nth column versus the first", default=-1)
p.add_argument("--runav",type=int,help="Use a Running average with N-values window", default=-1)
p.add_argument("--histogram", type=bool,help="Plot an histogram of the values", default=False)
p.add_argument("--cdf", type=bool,help="Plot the CDF of the values, only applicable if the --histogram flag is also given"  , default=False)
p.add_argument("--tu", type=str,help="Time units" , default="ns")
p.add_argument("--rmsf", type=bool, help="plot a rmsf run",default=False)
p.add_argument("--highlight", type=str, help="X values to highlight, give as a list of numbers separated by spaces, all surrounded by a set of quotation marks",default="")
p.add_argument("--forceyrange", type=str,help="Give two numbers separated by a space. Forces the boundary of the y axis to be twose two numbers",default="")
a = p.parse_args()

yrange=[]
force=a.forceyrange
if force!="":
    f=force.split()
    yrange.append(float(f[0]))
    yrange.append(float(f[1]))

#process highlight, we get the x coordinates that should be highlighted.
highstr=a.highlight.split()
xhigh=[]
for i in highstr:
    if a.highlight=="":
        break
    xhigh.append(float(i))

#The following is not very pretty, sorry about that.
prop="Property"
#if you don't want to tag the different numbers, just give a "" in this option.

tagslist=[]
if a.tags=="":
    for i in range(a.c):
        tagslist.append(str(i+1))
elif len(a.tags.split(","))==1:
    prop=a.tags
    for i in range(a.c):
        tagslist.append("")

else:
    prop=a.tags.split(",")[0]
    tagslist=a.tags.split(",")[1:]

runav=False
window=-1
if a.runav >0:
    runav=True
    window=a.runav
hist=False
cdf=False
density=True
if a.histogram:
    hist=True
    if a.cdf:
        density=False
#End the horrible user interface


extension=a.fname.split(".")[-1]
fin=open(a.fname,"r")

x=[]
ys=[]






if a.onlyplot==-1:
    for i in range(a.c):
        ys.append([])
else:
    ys.append([])

for line in fin:
    if line.startswith("@") or line.startswith("&") or line.startswith("#"):
        continue
    fields=line.split()
    x.append(float(fields[0])*a.tbf)
    for i,v in enumerate(fields[1:]):
        if a.onlyplot==-1:
            ys[i].append(float(v))
        elif (i+1)==a.onlyplot:
            ys[0].append(float(v))

#from the x coordinates we got before, we
#now get the y coordinates that are to be highlighted
#then we plot this pair with some exotic gliph
yhigh=[]
for i,val in enumerate(x):
    if a.highlight=="":
        break
    if val in xhigh:
        yhigh.append(ys[0][i]) #only the first column is highlightened

            

glyphs=["b-","r-","g-","k-","c-","m-","k--","b^-","ro-","g.-","c:"]        


if a.c>len(glyphs):
    print("only up to ", len(glyphs), "properties can be plot simultaneously")

z = b = np.arange(0, 3, .02)
c = np.exp(z)
d = c[::-1]

# Create plots with pre-defined labels.
fig, ax = plt.subplots()


if  a.xlabel=="Time":
    plt.xlabel('Time '+a.tu)
else:
    plt.xlabel(a.xlabel)

if yrange:
    axes = plt.gca()
    axes.set_ylim(yrange)

if a.rmsf:
    plt.xlabel("Residue number")
plt.ylabel(prop)
if hist:
    plt.xlabel(prop)
    plt.ylabel("Normalized frequency")
    
x2=x


ax.plot(xhigh,yhigh,"g*") 


for i,y in enumerate(ys):
    if a.runav>0:
        y=np.convolve(y, np.ones((a.runav,))/a.runav, mode='valid')
        ac=len(x)-len(y)
        x2=x[ac:]
    if a.histogram:
        print(len(x),len(y))
        if tagslist[i]!="":
            plt.hist(y,bins="auto",histtype="step",label=tagslist[i],cumulative=cdf, density=True)
        else:
            plt.hist(y,bins="auto",histtype="step",cumulative=cdf,density=True)
        continue
    if  tagslist[i]!="":
        ax.plot(x2,y,glyphs[i],label=tagslist[i])
    else:
        ax.plot(x2,y,glyphs[i])
ax.legend(loc='upper right')
plt.savefig(a.fname.replace("."+extension,".png"),dpi=600)

plt.show()


