# Software Carpentry Lab - AIMS-DISCnet 2018

### Matt Hilton - University of KwaZulu-Natal

This tutorial will take you through the process of setting up a command-line based Python
application that any user can install, using git for version control. Here, we develop a
code that can download light curve data obtained by the Kepler Space Telescope, in which
we will search for signs of transiting extrasolar planets.

Key:

    % you type something
    > console output that you should get back

Material that appears

```python
like 
this
does
```

should (usually) be copied and pasted into files where appropriate, as explained below.

## Getting started with git

If this is the first time you've used git, you may want to set these options - these 
would be used across all repositories (e.g., those on github, gitlab, sourceforge, etc.,
as well as locally on your machine). For example,

    % git config --global user.name "Your Name"
    % git config --global user.email "your@email.address"
 
We'll first create a bare, local repository. Repositories live in directories, so we will 
make one first - this will eventually contain all of our Python code for this project. 
Move into the directory when you're done.

    % mkdir planethunter
    % cd planethunter

Now let's make the bare repository by using the git init command:

    % git init
    > Initialized empty Git repository in /home/matty/Documents/Teaching/ZA-DISCnet-2018/planethunter/.git/ 

Git stores its data in a hidden folder called .git - to see this, you must use the 
`ls -a` command 

    % ls -a
    > . .. .git 

The `git status` command tells you whether you have uncommitted changes to your repository (or not), and what branch you are on. We'll discuss why branches are useful later - "master" here is the default. 
% git status
> On branch master
> 
> Initial commit
>
> nothing to commit (create/copy files and use "git add" to track) ```

Unsurprisingly, this tells us our repository is empty. Let's add some files. We're going to use this repository to hold a Python application that will download, plot, and fit light curve data from the Kepler satellite. This exercise could be done in an IPython/Jupyter notebook file, but we're going to set it up as a full blown Python application, to show how you would do that. Why? Because if you eventually end up analysing big data sets, you won't be running them in IPython notebooks. In this case, we may eventually want to run this code in parallel on thousands of light curves at the same time, on a cluster using MPI. 
We will follow a pretty standard layout for a Python project. First, let's add a README file that says what our project will do. Following github, we will actually use a file called README.md, where the extension indicates this is a Markdown file (e.g., https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) file. As the name suggests, Markdown is a simple plain text mark-up language (the most famous example of a mark-up language is HTML used in web pages). A handy tool for checking how your Markdown will look when rendered by a web browser can be found here: http://tmpvar.com/markdown.html.
You can create the README.md file in your favourite text editor (I use Kate and vim) - just be sure to save it in your planethunter/ directory. You can fill it with anything (we can edit it later), but here is a suggestion: 

# Planethunter 
A code for fetching Kepler light curve data, plotting it, and 
(eventually) fitting it with a planetary transit model. 

## Software needed 
Add python version and modules needed here e.g. 
* numpy (tested on version 1.14.1) 

## Installation 
How to install 

## Running Planethunter 
How to run 

## Comments, bug reports, suggestions etc. 
Please contact...
 
[if you want to do this using vim: 
% vim README.md 
Then press the 'i' key to enable editing, and copy and paste in the above text ('Ctrl-V' or 'shift-insert'). Press 'Esc' to exit editing mode, then type ':x' to save. If you want to quit vim without saving, type ':q!']
Now let's add our README.md file to the repository 
% git add README.md 
Now, when you use the git status command, it reports that there are changes to check in: 
% git status
> On branch master
> 
> Initial commit
> 
> Changes to be committed:
> (use "git rm --cached <file>..." to unstage)
>
> new file: README.md 
Our changes are only saved to the repository once we commit them. We can do this by: 
% git commit -m "Added README.md file" 
Here the -m switch is followed by a message. Alternatively you can commit changes with git commit -a, which will then open a text editor (vim is the default, but this can be changed) in which you can type your commit message. Either way, this allows you to keep track of the changes you made between each revision of the files in the repository. You can see these by doing 
% git log
> commit 47d7d7f1af97f23e1530114c9c5375e032a935db
> Author: Matt Hilton <mattyowl@gmail.com>
> Date: Mon Jun 11 09:19:36 2018 +0200
> 
> Added README.md file 
Git has many other commands, which you can see using 
% git help 
You can use this to get detailed information on each command, e.g., the commit command we just used: 
% git help commit 
will tell you about the -m and -a command line switches (among others).
Creating a python package
We will need to add a bunch of other files and directories to set up our Planethunter application. This is the layout we'll use for our python application, with a brief description of what each file will (ultimately) do: 

Directories:
bin/ [this will contain our executable script that will ultimately be run by the user of our application]
planethunter/ [evenually this will contain .py files used by our application] 
Files:
bin/planethunter [this will be our executable (python) script that the user of our application runs]
planethunter/__init__.py [note the double underscore __]
planethunter/lightCurveTools.py [eventually this will contain code for reading and plotting light curves]
setup.py [this will be the install script for our python application]
MANIFEST.in [this is a file that will be used by the setup.py script later]
README.md [you should have already made this one - see above] 

First, create the bin/ and planethunter/ directories, and then we'll create placeholder files. Let's look at each of these in turn... 
bin/planethunter
This will be our executable (python) script. Place the following in it for now: 

#!/usr/bin/env python3
""" 
Planethunter 
"""
print("This doesn't do anything yet!")

The first line begining #! (https://en.wikipedia.org/wiki/Shebang_(Unix)) tells the (Unix-like) operating system how to run the script: /usr/bin/env python3 finds the location of the python3 interpreter on the system and executes it (by convention, /usr/bin/env python should find and execute the python 2.x interpreter - we aren't using that for this exercise, but it ought to also work). 
The text inside the triple quotes """ """ is a docstring. You should use these extensively to document your code, in particular for functions and classes (we will return to this later). Docstrings are what you see when you use the help command inside the python3 or ipython interpreter. 
planethunter/__init__.py
This initializes the planethunter python package, and allows sub-directories (which we don't have, but may want to add later) to be identified as modules within the package (see https://docs.python.org/3/tutorial/modules.html#packages). Place the following in it for now: 

""" 
Planethunter - a python application for playing with Kepler data 
"""
from . import lightCurveTools 
__version__ = 'git'

Again, this starts with a docstring. It then imports the lightCurveTools module (which we'll create next), so that it is possible to do import planethunter and then access planethunter.lightCurveTools. Finally, we have __version__, which is the standard way of declaring the version number of your module in Python (see https://www.python.org/dev/peps/pep-0396/). For now we have written simply 'git', but this could easily say, e.g., '1.14.1' if that was the version number of the code that we decided to release. 
planethunter/lightCurveTools.py
This will contain our routines for actually doing analysis of light curves. Later, we will add routines to load them and plot them. For now, let's just create a file with a not-very-informative docstring

""" 
Tools for handling Kepler light curves - part of Planethunter 
"""

setup.py
This is the standard name for the script used to install Python packages, and these days it is usually handled by the setuptools package (https://setuptools.readthedocs.io/en/latest/). The setup.py script is very powerful, and can be made to, e.g., compile and build C extensions from source code. It can even handle and install dependencies (via pip; https://pypi.org/project/pip/). For now, let's just put in the most basic thing we can, which is suitable for a pure python package like Planethunter: 

# Planethunter install script 

import os
from distutils.core import setup
 
setup(name='planethunter',
      version="git",
      url=None,
      author='Your Name',
      author_email='your@email.here',
      description='Tool for finding planets in Kepler light curve data.',
      long_description="""A longer description of what this thing does.""",
      packages=['planethunter'],
      scripts=['bin/planethunter'], 
)

Now commit these changes to your git repository, remembering to add the files first (use git status to check that you have done so, if you're unsure). 
Installation, running the code, and making a source code distribution
We now have a code that does nothing, but which we can install. There are several ways to accomplish this, depending on your OS and whether you have root access or not, but the following should work: 
% python3 setup.py install --user
> running install
> running build
> running build_py
> creating build/lib
> creating build/lib/planethunter
> copying planethunter/__init__.py -> build/lib/planethunter
> copying planethunter/lightCurveTools.py -> build/lib/planethunter
> running build_scripts
> creating build/scripts-3.5
> copying and adjusting bin/planethunter -> build/scripts-3.5
> changing mode of build/scripts-3.5/planethunter from 664 to 775
> running install_lib
> creating /home/matty/.local/lib/python3.5/site-packages/planethunter
> copying build/lib/planethunter/__init__.py -> /home/matty/.local/lib/python3.5/site-packages/planethunter
> copying build/lib/planethunter/lightCurveTools.py -> /home/matty/.local/lib/python3.5/site-packages/planethunter
> byte-compiling /home/matty/.local/lib/python3.5/site-packages/planethunter/__init__.py to __init__.cpython-35.pyc
> byte-compiling /home/matty/.local/lib/python3.5/site-packages/planethunter/lightCurveTools.py to lightCurveTools.cpython-35.pyc
> running install_scripts
> copying build/scripts-3.5/planethunter -> /home/matty/.local/bin
> changing mode of /home/matty/.local/bin/planethunter to 775
> running install_egg_info
> Writing /home/matty/.local/lib/python3.5/site-packages/planethunter-git.egg-info 
The output from running the command tells you exactly what it has done: it has installed the package under $HOME/.local (i.e., in your home directory). Assuming that this has worked as expected, then you should be able to change to any other directory on your system, and then run the planethunter command, e.g., 
% cd
% planethunter
> This doesn't do anything yet! 
(Note: the above works on Ubuntu, but does not work on the AIMS lab computers - first you must type export PATH=$HOME/.local/bin:$PATH in the terminal from which you want to run planethunter)
Not very exciting... but the power of this approach is that it provides you with a way to distribute your software to your friends (or easily install it on other machines that you want to run it on). To do that, let's create another file, and add it to our git repository while we're at it. 
MANIFEST.in
The only reason to make this file at this stage is because we've used a non-standard name for the README file. You can use MANIFEST.in to include other directories or content in the source archive that will be built by setup.py (in a moment) that isn't specified in the setup.py file itself (e.g., a directory containing documentation or examples of how to use your code). For now, just paste in:

include README.md

Now add and commit it to the git repository 
% git add MANIFEST.in
% git commit -m "Added MANIFEST.in" 
We can now make a source archive (.tar.gz) that we can copy elsewhere and use to install our code: 
% python3 setup.py sdist
> running sdist
> running check
> warning: check: missing required meta-data: url
> 
> warning: sdist: standard file not found: should have one of README, README.txt
> 
> reading manifest template 'MANIFEST.in'
> writing manifest file 'MANIFEST'
> creating planethunter-git
> creating planethunter-git/bin
> creating planethunter-git/planethunter
> making hard links in planethunter-git...
> hard linking README.md -> planethunter-git
> hard linking setup.py -> planethunter-git
> hard linking bin/planethunter -> planethunter-git/bin
> hard linking planethunter/__init__.py -> planethunter-git/planethunter
> hard linking planethunter/lightCurveTools.py -> planethunter-git/planethunter
> Creating tar archive
> removing 'planethunter-git' (and everything under it) 
This complains that we don't have a README file (we have README.md instead) - but we can ignore that. You should find that a dist directory (short for 'distribution') has appeared, and contains a file called planethunter-git.tar.gz. This is a source archive that you can distribute to your friends, to share your exciting and useful code (this is also the kind of file that you could eventually upload to the Python Package Index: https://pypi.org/). 
Now we should do something to make our application actually useful... 
Adding more code
Let's add some routines to lightCurveTools.py that will allow us to do something useful with the data. Here is the revised code:

"""

Tools for handling Kepler light curves - part of Planethunter

"""

import os
import urllib
import astropy.table as atpy
from scipy import ndimage
import numpy as np

#------------------------------------------------------------------------------
def fetchLightCurveData(KICID, cacheDir = None):
    """Fetches processed Kepler light curve data for the star with the given 
    KIC ID number (KICID, which should be an int) from the internet.
    
    For the purposes of this exercise, this will download only the first light
    curve it finds from the year 2010, but this routine could easily be adapted
    to download all of the light curves for a given object.
    
    The files are downloaded and stored under cacheDir. If this is not given,
    a directory called KeplerCache will be created in the current directory, 
    and the files will be stored there.
    
    Returns True if successful, False if not
    
    """
    
    if cacheDir == None:
        cacheDir="KeplerCache"
    
    if os.path.exists(cacheDir) == False:
        os.makedirs("KeplerCache")
    
    # Need to add leading zeros
    KICStr="%09d" % (int(KICID))
    
    # We'll store only a single light curve in the cache, to make life easier
    # This would need to be changed to get all of the data
    outFileName=cacheDir+os.path.sep+KICStr+".fits"
    if os.path.exists(outFileName) == True:
        return True
    
    # Find the light curves
    # See this page: https://archive.stsci.edu/kepler/publiclightcurves.html
    baseURL="http://archive.stsci.edu/pub/kepler/lightcurves/"
    url=baseURL+KICStr[:4]+"/"+KICStr
    
    # The directory listing from the webserver will end up in this file
    tmpFileName=cacheDir+os.path.sep+"dirListing.html" 
    urllib.request.urlretrieve(url, filename = tmpFileName)
    
    # Fetch the first long cadence light curve taken in 2010 that we see
    if os.path.exists(tmpFileName) == True:
        
        inFile=open(tmpFileName, "r")
        lines=inFile.readlines()
        inFile.close()
        
        foundLine=False
        for line in lines:
            if line.find("kplr") != -1 and line.find("-2010") != -1 and \
                line.find("_llc.fits") != -1:
                foundLine=True
                break
        
        if foundLine == False:
            return False
        
        urlToFetch=url+"/kplr"+line.split("kplr")[1].split('"')[0]
        print("... downloading from %s ..." % (urlToFetch))
        urllib.request.urlretrieve(urlToFetch, filename = outFileName)
    
    if os.path.exists(outFileName) == True:
        return True
    else:
        print("... failed to fetch light curve for KICID = %d ..." % (KICID))
        return False

#------------------------------------------------------------------------------
def loadLightCurve(KICID, whiten = False, medianWindowDays = 1.0, 
                   cacheDir = None):
    """Given a KICID (an int), load the cached data (see fetchLightCurveData), 
    and optionally divide through by a running median to both "normalise" and
    whiten the data.
    
    medianWindowDays sets the number of days over which the rolling median is 
    subtracted.
    
    We estimate the flux error here from the 3-sigma clipped standard 
    deviation of the scatter of the whitened data.
    
    Returns timeArr, fluxArr, fluxErrArr
    
    """

    if cacheDir == None:
        cacheDir="KeplerCache"

    KICStr="%09d" % (int(KICID))
    fileName=cacheDir+os.path.sep+KICStr+".fits"
                
    tab=atpy.Table().read(fileName)
    tab.sort('TIME')
        
    fluxArr=tab['PDCSAP_FLUX']
    timeArr=tab['TIME']
    fluxErrArr=tab['PDCSAP_FLUX_ERR']
    mask=np.logical_not(np.logical_or(np.isnan(timeArr), np.isnan(fluxArr)))
    timeArr=np.array(timeArr[mask])
    fluxArr=np.array(fluxArr[mask])
    fluxErrArr=np.array(fluxErrArr[mask])
                  
    # Optionally "whiten" the data - by dividing through by running median
    if whiten == True:
        medWindowPoints=int(round(medianWindowDays/(timeArr[1]-timeArr[0])))
        medFluxArr=ndimage.median_filter(fluxArr, medWindowPoints)
        fluxArr=fluxArr/medFluxArr
    
    # Chuck out points where exactly == 1 
    # (median filtering related - one point in these bins probably)
    mask=np.not_equal(fluxArr, 1)
    fluxArr=fluxArr[mask]
    fluxErrArr=fluxErrArr[mask]
    timeArr=timeArr[mask]
    
    # Estimate of flux error
    sigma=1e6
    meanFlux=np.mean(fluxArr)
    for i in range(10):
        mask=np.less(abs(fluxArr-meanFlux), 3*sigma)
        sigma=np.std(fluxArr[mask])
        meanFlux=np.mean(fluxArr[mask])
    fluxErrArr[:]=sigma
        
    return timeArr, fluxArr, fluxErrArr

Notice again that we provide a docstring for each function. This may not be the greatest documentation in the world (or the greatest code), but it's far better than nothing, and we can fix it later if we want.
Copy and paste the code above into lightCurveTools.py, and check that you can install the code without any errors (i.e. % python3 setup.py install --user). Don't commit these changes to your git repository yet - first you should check to see that the code works as expected (you should never check in code that you know is broken, especially if you are working on a project with other people). 
The new routines won't allow our executable script (planethunter) to do anything as yet, but we can test out our lightCurveTools module by using IPython interactively. Change to a directory outside of your git repository (e.g., your home directory), and start up IPython. We'll then use our new Python module to fetch a light curve for the star KIC 8191672, around which the planet Kepler-5b is found (e.g., http://www.openexoplanetcatalogue.com/planet/Kepler-5%20b/): 
% ipython3
> Python 3.5.2 (default, Nov 23 2017, 16:37:01) 
> Type "copyright", "credits" or "license" for more information. 
> IPython 2.4.1 -- An enhanced Interactive Python.
> ? -> Introduction and overview of IPython's features.
> %quickref -> Quick reference.
> help -> Python's own help system.
> object? -> Details about 'object', use 'object??' for extra details. 

% from planethunter import lightCurveTools as lct 
% lct.fetchLightCurveData(8191672)
> ... downloading from http://archive.stsci.edu/pub/kepler/lightcurves/0081/008191672/kplr008191672-2010078095331_llc.fits ...
> Out[2]: True 
If, as above, lct.fetchLightCurveData returned True, then you should find a KeplerCache directory containing a .fits table file has appeared in the current directory.
% ls KeplerCache
> 008191672.fits 
You can also try out the routine for loading the data, and plot it while inside the IPython session. 
% timeArr, fluxArr, fluxErrArr=lct.loadLightCurve(8191672) 
% import pylab as plt 
% plt.ion() 
% plt.plot(timeArr, fluxArr, '.')
% plt.xlabel("Time (days)")
% plt.ylabel("Flux")
This should produce a plot like this Fig. 1 below. The dips every ~3.5 days are due to a planet (Kepler-5b) passing in front of the star. Notice however that there is longer term variation in the flux of the star itself - i.e., its flux is not constant, and the noise (scatter around the average) is not white (the average is moving - i.e., there is some kind of 1/f noise).

The loadLightCurve function has an option to normalise and whiten the data (i.e., flatten out the varying flux of the star to make it easier to find the transits due to the planet). It does this by dividing the light curve through by a running median. Let's try that (after closing the previous plot): 
% timeArr, fluxArr, fluxErrArr=lct.loadLightCurve(8191672, whiten = True) 
% plt.plot(timeArr, fluxArr, '.')
% plt.xlabel("Time (days)")
% plt.ylabel("Normalised Flux")
Fig. 2 shows the result that you should get. 

You can see this looks much more like the idealised plots / animations in the lecture slides that show the flux from the star to be constant, only dipping when the planet passes in front of it. This will be much easier to fit with a simple model than the unwhitened, non-normalised data. 
If everything is working as expected, now would be the time to commit your changes to the git repository.
Making the planethunter executable useful - command line options
We now have a usable lightCurveTools module - let's apply it to the planethunter script that the user of our package can run. Here we'll look at adding command line options, so that the user can use the script to download and plot a Kepler light curve, with or without the normalisation/whitening applied. 
The first thing to do is delete the message we had in there before. We'll then use the argparse module to handle the command line interface (this is fancy; you could also use plain sys.argv if you wanted - but a nice feature of the argparse module is that if the user runs a program with the -h flag, it will print a help message). So, the script should now start like this: 

#!/usr/bin/env python3
"""

Planethunter

"""

import sys
import pylab as plt
import argparse
from planethunter import lightCurveTools as lct

if __name__ == '__main__':

    parser=argparse.ArgumentParser("planethunter")
    parser.add_argument("KICID", help = """KIC ID number of the star of interest.""")
    parser.add_argument("-w", "--whiten", dest = "whiten", action = "store_true", 
                        help = """Normalise and whiten the light curve.""")

    args=parser.parse_args()

    try:
        KICID=int(args.KICID)
    except:
        print("Error - KICID must be a number")
        sys.exit()

Notice that we check the user's input in the try... except... block, and instead of throwing an exception, we just print a message and exit. There is no real reason to do this, other than this shows to the user that they entered an invalid value in a fairly friendly way (if we just let it throw the Python exception, the user may instead think that there is a bug in the code). 
After you install the updated code (using the setup.py script again), you will now find that you can run the planethunter script like this  (don't do this in the directory that holds your git repository): 
% planethunter 8191672 
The example code above shows you how to access the arguments that have been passed into your program. Now extend the code so that it uses the routines in your lightCurveTools module to load and plot a light curve (like we did using IPython in the section above). For now, perhaps just make the code save the plot as 'plot.png' in your current directory. 
For the whiten switch (-w), you will find that args.whiten is True when the user runs e.g. 
% planethunter 8191672 -w 
and that args.whiten = False otherwise. Adapt your code accordingly, such that the user gets a light curve plot that is either normalised and whitened, or not, depending on whether they used the -w switch or not. 
Once you are happy with the results (compare them to Fig. 1 and Fig. 2), commit your changes to the repository. 
Git branches
Now would be a good time to start thinking about how to fit the data. For the sake of this exercise, we're going to do this on a new branch in our git repository. After creating and switching to a new branch, changes committed in our new branch will not be reflected in the master branch that we have been using so far. Once we are satisfied with our new branch, at a later stage we can then merge those changes into the master branch.
Branches are particularly useful if several people are working on (or using) the same repository. For example, one person could open a new branch in order to fix a bug in one part of the code, while others could continue working in a different branch independently. Later on, they can merge their changes together in the master branch. 
Another example would be the case where you want to make a major change to how the code works. Say you had a Python 2.x application and had made the descision to port to Python 3.x - a natural way to do this would be to start a python3 branch, make all the necessary changes, and then merge this back into master once complete and tested.
To create a new branch, we use the git checkout command with the -b argument:
% git checkout -b fitting
> Switched to a new branch 'fitting' 
If you're ever unsure what branch you are currently on, you can use the git status command:
% git status
> On branch fitting
> Untracked files:
>   (use "git add <file>..." to include in what will be committed)
> 
>         MANIFEST
>         build/
>         dist/
> 
> nothing added to commit but untracked files present (use "git add" to track)
Now if we use git commit, our changes will reflect on the fitting branch, but not on master. You can switch between branches using the git checkout command, e.g.,
% git checkout master
> Switched to branch 'master'
% git checkout fitting
> Switched to branch 'fitting'
Make sure you are back on the fitting branch before continuing.
One way to detect exoplanets is to fit a model for a transiting object to the light curve data. When the planet is in front of the star, the flux from the star dips - otherwise, we can assume that the flux from the star is constant (not all stars, nor our data, necessarily behave this way - but the normalising and whitening step in our loadLightCurve routine makes this so for at least KIC 8191672). So, a reasonable model to try would be one in which the flux immediately dips when a transit occurs, but is 1 otherwise. The following code describes such a model:

def dipModel(t, p, t0, d, f0):
    """A simple model of the dip in a light curve caused by a transit. Assumes
    that the light curve that we would fit this to has been whitened and
    normalised.
    
    Here, t is a an array of time values (for Kepler data, this would be in 
    days).
    
    Parameters:
        p   - period
        t0  - time at the centre of the transit
        d   - transit duration
        f0  - (normalised) flux at the centre of the transit
    
    Returns an array of model flux values corresponding to t.
    
    """

    # Flux is only not 1 when transits occur
    modelFlux=np.ones(len(t))
    numCycles=np.floor(t.max()-t0)
    transitTimes=t0+np.arange(numCycles)*p
    for tt in transitTimes:
        mask=np.logical_and(np.greater(t, tt-d/2.), np.less(t, tt+d/2.))
        modelFlux[mask]=f0
    
    return modelFlux

Note that we didn't specify any units in the docstring - but p, t0, d would all be in units of days, if we feed in timeArr from one of our Kepler light curves.
Add the above routine to your code: you can choose where you want to put it. You could add it to lightCurveTools, or you could add a new module (called, e.g., fitTools - if so, remember to also update __init__.py). The choice is yours.
To test it out, you can try the following in an IPython session (assuming you are in the same directory as KeplerCache/) - adjust this according to where you decided to place the dipModel routine:
% from planethunter import lightCurveTools as lct
% from planethunter import fitTools
% timeArr, fluxArr, fluxErrArr=lct.loadLightCurve(8191672, whiten = True)
% import pylab as plt
% plt.ion()
% plt.plot(timeArr, fluxArr, '.')
% plt.plot(timeArr, fitTools.dipModel(timeArr, 3.5485, 353.55, 0.5, 0.993), 'k-')
In the last line, we've dialed in the known period for the planet Kepler-5b, and read off the values for t0, f0 from looking at the data (the value for d is just a guess). This should give you a plot like Fig. 3 below.
If you are happy that your code is correct and works as expected, commit your changes to the repository (remembering to git add any new files first, e.g., fitTools.py, if you created them).
% git commit -a
> [fitting 77ae77d] Added fitTools.py with simple dip model.
> 2 files changed, 39 insertions(+)
> create mode 100644 planethunter/fitTools.py
Suppose we're sufficiently happy with our progress on the fitting branch, and want to merge the changes into the master branch. This is how we would do that:
% git checkout master
> Switched to branch 'master'
% git merge fitting
> Updating 556f5f2..77ae77d
> Fast-forward
>  planethunter/__init__.py |  2 ++
>  planethunter/fitTools.py | 37 +++++++++++++++++++++++++++++++++++++
>  2 files changed, 39 insertions(+)
>  create mode 100644 planethunter/fitTools.py
Your master and fitting branches now contain the same code. Switch back to the fitting branch before continuing by doing
> git checkout fitting
> Switched to branch 'fitting'


Fitting the data
You should now feel free to experiment with applying what you have learned in the previous couple of days to actually fitting a model to the light curve data. An obvious place to start would be to try χ2 minimisation or perhaps MCMC (if anyone gets the latter to work, let me know... one thing you will probably want to change first is to fit for a phase offset rather than t0). See if you can add routines to the planethunter script and/or the other modules in the package to fit light curve data and find at least the period of the exoplanet, and report some statistic that indicates the goodness of fit. Before trying to automate it, you might want to check your likelihood calculation by dialing in some values around the best-fit values of the parameters first (e.g., plot χ2 versus period).
One other kind of plot that is useful for this project is the transit-centred phased light curve. The code below shows how you can make this, if you have a best-fit model. This example is just for the parameters we previously used in Fig. 3:
% p, t0, d, f0=3.5485, 353.55, 0.5, 0.993
% phase=timeArr/p
% phase=phase % 1
% phaseCentre=t0/p % 1
% phase=phase-phaseCentre
% modelPhase=np.linspace(-0.5, 0.5, 1000)
% modelFlux=fitTools.dipModel(modelPhase*p, p, 0, d, f0)
% plt.plot(phase, fluxArr, '.')
% plt.plot(modelPhase, modelFlux, 'k-')
% plt.xlim(-0.5, 0.5)
% plt.xlabel("Phase")
% plt.ylabel("Normalised Flux")
Fig. 4 shows how this should look - here we can clearly see that our guess for the value of d (the transit duration) was too large.

This kind of plot is so useful, that you should probably add a routine that does this to planethunter...
What next?
There are many topics that we haven't covered in this tutorial. In terms of git, we have not touched on interacting with remote repositories, such as hosted by github. You would do this with the git push and git pull commands - see this tutorial, for example: https://swcarpentry.github.io/git-novice/. Github itself also has excellent documentation.
We also haven't touched on reverting changes to your repository. You can find a handy guide for doing that kind of thing here: https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things
In terms of the planethunter code itself, here are some other things that you could investigate:
Running the code on light curves of other stars
Stitching together multiple light curve files for the same star (each individual .fits file covers 90 days) to look for longer period planets
Multi-planet systems (the model above only includes a single planet)
Planets around binary stars (where two stars themselves eclipse each other)
Running the code in parallel on many light curves at the same time (e.g., using MPI)
Useful links
Pro Git: https://git-scm.com/book/en/v2 [a full book on git, with a Creative Commons license]
The Python Standard Library: https://docs.python.org/3/library/index.html
Documentation for the scipy.optimize module: https://docs.scipy.org/doc/scipy/reference/optimize.html [one option for fitting]
Kepler objects of interest: https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative [the kepID column has the KIC number you would need to download the light curve with our code]
Information on Kepler data products: http://keplerscience.arc.nasa.gov/data-products.html
The manual for the Kepler data archive products: http://archive.stsci.edu/kepler/manuals/archive_manual.pdf [read this if you want details on the processing that was done to the light curve data that we are using]
