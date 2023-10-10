import os
import shutil
import sys
from enum import Enum
from datetime import datetime
import time
import argparse
import logging
import dirTree



class Action(Enum):
    ADD = 1
    REMOVE = 2

def validation(args):
    
    if not os.path.exists(args.origin):
        logging.error('Origin directory does not exists.')
        return False
    if not os.path.exists(args.replica):
        logging.error("Replica directory does not exists.")
        return False
    if args.timer < 0:
        logging.error("The timer must be at least 0 seconds.")
        return False
    if not os.path.exists(args.log):
        logging.error("Log file does not exists.")
        return False
    return True
#the paths here do NOT contain the origin and replica prefix
def getDifferences(origin,replica):
    adds = []
    removes = []
    update = []
    pairs = []
    for file in origin:
        if file not in replica:
            adds.append(os.path.join(args.origin,file))
        
    for indexReplica,file in enumerate(replica):
        if file not in origin:
            removes.append(os.path.join(args.replica,file))
        if file in origin:
            indexOrigin = origin.index(file)
            pairs.append((indexOrigin,indexReplica))

        for pair in pairs:
            modifTimeOrigin = os.path.getctime(os.path.join(args.origin,origin[pair[0]]))
            modifTimeReplica = os.path.getctime(os.path.join(args.replica,replica[pair[1]]))

        #not tested
        

def main(args):
    while True:
        try:
            time.sleep(args.timer)
            originTree = dirTree.dirTree(args.origin)
            replicaTree = dirTree.dirTree(args.replica)
            
        except KeyboardInterrupt:
            print("Application stopped. Thank you.")
            return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Syncronize two directories")
    parser.add_argument('origin',type=str,help='Location of folder to be cloned')
    parser.add_argument('replica',type=str,help='Location of the replica directory')
    parser.add_argument('timer',type=int,help='Time interval in between checks in seconds')
    parser.add_argument('log',type=str,help='Location of the log file')
    args = parser.parse_args()
    if validation(args):
        main(args)
    