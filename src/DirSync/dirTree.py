import os
import sys


class dirTree:
    def __init__(self,path):
        self.path = path
        self.children = []
        try:
            for file in os.listdir(path):
                self.children.append(dirTree(os.path.join(path,file)))
        except NotADirectoryError:
            print("")

    def addChild(self,file):
        self.children.append(file)

    def removeChild(self,file):
        self.children.remove(file)
    

    def printTree(self):
        for elem in self.children:
            print(elem.path)

            elem.printTree()

    @staticmethod
    def getTree(root):
        tree = []
        for elem in root.children:
            tree.append(elem.path)
            tree += dirTree.getTree(elem)
        
        return tree


if __name__ == "__main__":
    root = dirTree(sys.argv[1])
    
    print(root.printTree())