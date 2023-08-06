""" Loading module and variables """

import os,sys

def showhelp():
    """
    Show help menu if requested.
    """
    print("")
    print("-----------------------------------------------------------")
    print("   Quasar Spectra Velocity Scanner")
    print("-----------------------------------------------------------")
    print("")
    print("usage: qscan <spectrum> [--args]")
    print("")
    print("optional arguments:")
    print("")
    print("   --atom        Use custom atom.dat")
    print("   --dv          Plotted velocity disperion (default: 700)")
    print("   --fort        Input fort.13 file")
    print("   --list        List of metal transitions")
    print("   --zabs        Start absorption redshift (default: 1)")
    print("")
    print("-----------------------------------------------------------")
    print("")
    quit()
    
def makeatomlist(atompath):
    """
    Store data from atom.dat.

    Parameters
    ----------
    atompath : str
      Path to atom.dat file.
    """
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    atomlist    = np.empty((0,6))
    atomdat     = np.loadtxt(atompath,dtype='str',delimiter='\n')
    for element in atomdat:
        l       = element.split()
        i       = 0    if len(l[0])>1 else 1
        species = l[0] if len(l[0])>1 else l[0]+l[1]
        wave    = 0 if len(l)<i+2 or isfloat(l[i+1])==False else l[i+1]
        f       = 0 if len(l)<i+3 or isfloat(l[i+2])==False else l[i+2]
        gamma   = 0 if len(l)<i+4 or isfloat(l[i+3])==False else l[i+3]
        mass    = 0 if len(l)<i+5 or isfloat(l[i+4])==False else l[i+4]
        alpha   = 0 if len(l)<i+6 or isfloat(l[i+5])==False else l[i+5]
        if species!='end' and species[0].isalpha()==True: 
            atomlist = np.vstack((atomlist,[species,wave,f,gamma,mass,alpha]))
    return atomlist

def makecustomlist(original,atompath):
    '''
    Get atomic data from selected atomID

    Parameters
    ----------
    original : numpy.array
      Original atom.dat data
    atompath : str
      Path to custom list of metal transitions

    Return
    ------
    atomlist : numpy.array
      New atomic data list with selected transitions only
    '''
    atomlist = np.empty((0,6))
    atomdat  = np.loadtxt(atompath,dtype='str',ndmin=2)
    for atomID,wrest in atomdat:
        # Identify targeted ion and check list of transitions available in atom.dat
        imet = numpy.where(original[:,0]==atomID)[0]
        # Define target transition parameter list
        target = [0,0,0,0,0,0]
        # List through all transitions found for that ion
        for i in imet:
            # Define transition parameters
            element    = original[i,0]
            wavelength = original[i,1]
            oscillator = original[i,2]  
            gammavalue = original[i,3]
            mass       = original[i,4]
            qcoeff     = original[i,5]
            # Condition 1: transition wavelength must be close to targeted transition
            cond1 = abs( float(wavelength) - float(wrest) ) < 1
            # Condition 2: oscillator strength should be greater than previously found
            cond2 = float(oscillator) > float(target[2])
            # If both condition satisfy, set transition as main target
            if cond1 and cond2:
                target = [element,wavelength,oscillator,gammavalue,mass,qcoeff]
        atomlist = np.vstack((atomlist,target))
    return atomlist

def variables():
    """
    Set up global variable and key map environment.
    """
    if len(sys.argv)==1 or '--help' in sys.argv or '-h' in sys.argv:
        showhelp()
    
    # Setup graphic settings
    
    rc('font', size=10, family='sans-serif')
    rc('axes', labelsize=10, linewidth=0.2)
    rc('legend', fontsize=10, handlelength=10)
    rc('xtick', labelsize=10)
    rc('ytick', labelsize=10)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    
    # Empty key map
    
    keyMaps = [key for key in rcParams.keys() if 'keymap.' in key]
    for keyMap in keyMaps:
        rcParams[keyMap] = ''
    
    # Define tables and variables
    
    v            = type('v', (), {})()
    v.c          = 299792.458
    v.shift      = -82
    v.datapath   = os.path.abspath(__file__).rsplit('/',1)[0] + '/data/'
    v.atmolines  = np.loadtxt(v.datapath+'atmolines.dat')
    v.hydrolist  = makeatomlist(v.datapath+'hydrolist.dat')[::-1]
    v.hydroreg   = np.zeros((len(v.hydrolist),4),dtype=object)
    v.hydrovoigt = np.array([[0,np.empty((0,5),dtype=object)] for i in range(len(v.hydrolist))])
    v.dtohflag   = 0
    v.atmosphere = 0
    v.wblendmin  = None
    v.wblendmax  = None
    v.blendflag  = 0
    v.z          = 0.01
    v.anchor     = None
    v.flag13     = 'no'
    v.N,v.b      = 19,10
    v.mode       = 'scan'
    v.edgeforce  = []
    v.dvprev     = None
    
    # Checking arguments
    
    argument = np.array(sys.argv, dtype='str')

    v.atom = v.datapath+'atom.dat'
    if '--atom' in sys.argv:
        k = np.where(argument=='--atom')[0][0]
        v.atom = makeatomlist(argument[k+1])
    
    v.dv = 700.
    if '--dv' in sys.argv:
        k = np.where(argument=='--dv')[0][0]
        v.dv = float(argument[k+1])

    v.fort = None
    if '--fort' in sys.argv:
        k = np.where(argument=='--fort')[0][0]
        v.fort = argument[k+1]
        
    v.zabs = v.zprev = 0.1
    if '--zabs' in sys.argv:
        k = np.where(argument=='--zabs')[0][0]
        v.zabs = v.zprev = float(argument[k+1])
        
    v.metallist  = makeatomlist(v.datapath+'metallist.dat')[::-1]
    v.metalreg   = np.zeros((len(v.metallist),4),dtype=object)
    v.metalvoigt = np.array([[0,np.empty((0,5),dtype=object)] for i in range(len(v.metallist))])
    if '--list' in sys.argv:
        k = np.where(argument=='--list')[0][0]
        v.metallist = makecustomlist(v.atom,argument[k+1])[::-1]
        v.metalreg   = np.zeros((len(v.metallist),4),dtype=object)
        v.metalvoigt = np.array([[0,np.empty((0,5),dtype=object)] for i in range(len(v.metallist))])
        
    return v

if sys.argv[0].split('/')[-1]!='qscan':
    pass
elif len(sys.argv)==1 or '--help' in sys.argv or '-h' in sys.argv:
    showhelp()
elif os.path.exists(sys.argv[1])==False:
    print("ERROR: spectrum '"+sys.argv[1]+"' not found...")
    quit()
else:
    import re,numpy
    from matplotlib.pyplot import *
    from matplotlib        import rc
    from astropy.io        import fits
    from scipy.ndimage     import gaussian_filter1d
    setup = variables()
