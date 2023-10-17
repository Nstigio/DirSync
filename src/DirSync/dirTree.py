import os
import sys


class dirTree:
    def __init__(self,path):
        self.path = path
        self.children = []
        self.add = None
        self.remove = None
        self.update = None
        try:
            for file in os.listdir(path):
                self.children.append(dirTree(os.path.join(path,file)))
            
           # self.children.sort()
        except NotADirectoryError:
            pass

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
