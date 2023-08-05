''' 
Script to run flight simulations from the command line 
If MAPLEAF has been installed with pip, this script is accessible through the 'mapleaf' command
'''

import argparse
import os
import sys
import time
from typing import List

import MAPLEAF.IO.Logging as Logging
import MAPLEAF.IO.Plotting as Plotting
from MAPLEAF.IO import SimDefinition, getAbsoluteFilePath
from MAPLEAF.SimulationRunners import (ConvergenceSimRunner,
                                       OptimizingSimRunner, Simulation,
                                       runMonteCarloSimulation)
from MAPLEAF.SimulationRunners.Batch import main as batchMain


def buildParser() -> argparse.ArgumentParser:
    ''' Builds the command-line argument parser using argparse '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="""
    Run individual MAPLEAF simulations.
    Expects simulations to be defined by simulation definition files like those in ./MAPLEAF/Examples/Simulations 
    See ./SimDefinitionTemplate.mapleaf for definition of all possible options
    """)

    mutexGroup = parser.add_mutually_exclusive_group()
    mutexGroup.add_argument(
        "--converge", 
        action='store_true', 
        help="Runs the current simulation using successively finer time steps, attempting to provide a converged final location"
    )
    mutexGroup.add_argument(
        "--compareIntegrationSchemes", 
        action='store_true', 
        help="Attempts to converge the current simulation using a variety of classical integration schemes."
    )
    mutexGroup.add_argument(
        "--compareAdaptiveIntegrationSchemes", 
        action='store_true', 
        help="Attempts to converge the current simulation using a variety of adaptive time integration schemes"
    )
    mutexGroup.add_argument(
        "--plotFromLog", 
        nargs=2, 
        default=[], 
        metavar=("plotDefinition", "pathToLogFile"),
        help="plotDefinition works the same way as SimControl.plot entries in simulation definition files"
    )

    parser.add_argument(
        "--nCores",
        type=int,
        nargs=1,
        default=[1],
        help="Use to run Monte Carlo or Optimization studies in parallel using ray. Check whether ray's Windows support has exited alpha, or use only on Linux/Mac."
    )
    parser.add_argument(
        "--silent", 
        action='store_true', 
        help="If present, does not output to console - faster on windows"
    )
    parser.add_argument(
        "simDefinitionFile", 
        nargs='?', 
        default="MAPLEAF/Examples/Simulations/NASATwoStagOrbitalRocket.mapleaf",
        help="Path to a simulation definition (.mapleaf) file. Not required if using --plotFromLog"
    )

    return parser

def findSimDefinitionFile(providedPath):
    if os.path.isfile(providedPath):
        return providedPath

    # Check if it's a relative path that needs to be made absolute
    possibleRelPath = providedPath
    absPath = getAbsoluteFilePath(possibleRelPath)
    if os.path.isfile(absPath):
        return absPath
    
    # Check if it's an example case
    if possibleRelPath[-8:] != ".mapleaf":
        # If it's just the case name (ex: 'Staging') add the file extension
        possibleRelPath += ".mapleaf"
    
    possibleRelPath = "MAPLEAF/Examples/Simulations/" + possibleRelPath
    absPath = getAbsoluteFilePath(possibleRelPath)
    if os.path.isfile(absPath):
        return absPath  

    print("ERROR: Unable to locate simulation definition file: {}!".format(providedPath))
    sys.exit()

def isOptimizationProblem(simDefinition) -> bool:
    try:
        simDefinition.getValue("Optimization.costFunction")
        return True
    except KeyError:
        return False

def isMonteCarloSimulation(simDefinition) -> bool:
    try:
        nRuns = float(simDefinition.getValue("MonteCarlo.numberRuns"))
        if nRuns > 1:
            return True
    except (KeyError, ValueError):
        pass

    return False

def isBatchSim(batchDefinition) -> bool:
    ''' Checks whether the file does not contain a 'Rocket' dictionary, and instead contains dictionaries that have a simDefinitionFile key  '''
    rootDicts = batchDefinition.getImmediateSubDicts("")

    for rootDict in rootDicts:
        if rootDict == 'Rocket' and 'Rocket.simDefinitionFile' not in batchDefinition:
            return False
    
    return True

def main(argv=None) -> int:
    ''' 
        Main function to run a MAPLEAF simulation. 
        Expects to be called from the command line, usually using the `mapleaf` command
        
        For testing purposes, can also pass a list of command line arguments into the argv parameter
    '''
    startTime = time.time()

    # Parse command line call, check for errors
    parser = buildParser()
    args = parser.parse_args(argv) 

    if len(args.plotFromLog):
        # Just plot a column from a log file, and not run a whole simulation
        Plotting.plotFromLogFiles([args.plotFromLog[1]], args.plotFromLog[0])
        print("Exiting")
        sys.exit()
     
    # Load simulation definition file
    simDefPath = findSimDefinitionFile(args.simDefinitionFile)
    simDef = SimDefinition(simDefPath)

    #### Run simulation(s) ####
    if isOptimizationProblem(simDef):
        optSimRunner = OptimizingSimRunner(simDefinition=simDef, silent=args.silent, nCores=args.nCores[0])
        optSimRunner.runOptimization()

    elif isMonteCarloSimulation(simDef):
        runMonteCarloSimulation(simDefinition=simDef, silent=args.silent, nCores=args.nCores[0])

    elif args.nCores[0] > 1:
        raise ValueError("ERROR: Can only run Monte Carlo of Optimization-type simulations in multi-threaded mode. Support for multi-threaded batch simulations coming soon.")

    elif isBatchSim(simDef):
        print("Batch Simulation\n")
        batchMain([ simDef.fileName ])

    elif args.converge or args.compareIntegrationSchemes or args.compareAdaptiveIntegrationSchemes: 
        cSimRunner = ConvergenceSimRunner(simDefinition=simDef, silent=args.silent)
        if args.converge:
            cSimRunner.convergeSimEndPosition()
        elif args.compareIntegrationSchemes:
            cSimRunner.compareClassicalIntegrationSchemes(convergenceResultFilePath='convergenceResult.csv')
        elif args.compareAdaptiveIntegrationSchemes:
            cSimRunner.compareAdaptiveIntegrationSchemes(convergenceResultFilePath='adaptiveConvergenceResult.csv')
    
    else: 
        # Run a regular, single simulation  
        simRunner = Simulation(simDefinition=simDef, silent=args.silent)
        simRunner.run()

    Logging.removeLogger()

    print("Run time: {:1.2f} seconds".format(time.time() - startTime))
    print("Exiting")

if __name__ == "__main__":
    main()
