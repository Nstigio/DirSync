import os
import shutil
import time
import argparse
import logging
import dirTree

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
fileHandler = logging.FileHandler('log.txt')
fileHandler.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
# Create a formatter and set it for the handler
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

def logs(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        action = func.__name__
        file = args[0]
        logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - action: {action} - file: {file}')
        return result
    return wrapper

def validation():
    
    if not os.path.exists(arguments.origin):
        logging.error('Origin directory does not exists.')
        return False
    if not os.path.exists(arguments.replica):
        logging.error("Replica directory does not exists.")
        return False
    if arguments.timer < 0:
        logging.error("The timer must be at least 0 seconds.")
        return False
    
    return True
   
def getDifferences(origin,replica):
    #the paths here do NOT contain the origin and replica prefix
    originList = [os.path.relpath(file,arguments.origin) for file in origin]
    replicaList = [os.path.relpath(file,arguments.replica) for file in replica]

    adds = []
    removes = []
    updates = []

    for file in originList:
        if file not in replicaList:
            adds.append(file)
        
    for file in replicaList:
        if file not in originList:
            removes.append(file)
        else:
            if not os.path.isdir(os.path.join(arguments.replica,file)):

                originModifTime = os.path.getmtime(os.path.join(arguments.origin,file))
                replicaModifTime = os.path.getmtime(os.path.join(arguments.replica,file))

                #originModifTime = originModifTime // 60 * 60 + 60
                #replicaModifTime = replicaModifTime // 60 *60 + 60

                if not originModifTime == replicaModifTime:
                    updates.append(file)
    
    return adds,removes,updates
            
def sync(adds,removes,updates):
    
    def sortOrder(path):
        return len(path.split(os.pathsep))
    @logs
    def add(file):
        if os.path.isdir(os.path.join(arguments.origin, file)):
            os.makedirs(os.path.join(arguments.replica, file), exist_ok=True)
        else:
            shutil.copy2(os.path.join(arguments.origin, file), os.path.join(arguments.replica, file))

    @logs
    def remove(file):
        if os.path.isdir(os.path.join(arguments.replica, file)):
            os.removedirs(os.path.join(arguments.replica, file))
        else:
            os.remove(os.path.join(arguments.replica, file))

    @logs
    def update(file):
        if os.path.isdir(os.path.join(arguments.origin, file)):
            os.makedirs(os.path.join(arguments.replica, file), exist_ok=True)
        else:
            shutil.copy2(os.path.join(arguments.origin, file), os.path.join(arguments.replica, file))
    
    adds.sort(key=sortOrder)
    removes.sort(key=sortOrder)
    updates.sort(key=sortOrder)

    if not len(adds) == 0:
        for file in adds:
            add(file)

    if not len(removes) == 0:
        for file in removes:
            remove(file)
            
    if not len(updates) == 0:
        for file in updates:
            update(file)

def main(arguments):
    
    while True:
        try:
            time.sleep(arguments.timer)
            originTree = dirTree.dirTree(arguments.origin)
            replicaTree = dirTree.dirTree(arguments.replica)
            
            adds,removes,update = getDifferences(dirTree.dirTree.getTree(originTree),dirTree.dirTree.getTree(replicaTree))

            sync(adds,removes,update)

        except KeyboardInterrupt:
            print("Application stopped. Thank you.")
            return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Syncronize two directories")
    parser.add_argument('origin',type=str,help='Location of folder to be cloned')
    parser.add_argument('replica',type=str,help='Location of the replica directory')
    parser.add_argument('timer',type=int,help='Time interval in between checks in seconds')
    arguments = parser.parse_args()
    if validation():
        main(arguments)
    