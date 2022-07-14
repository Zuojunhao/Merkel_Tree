import hashlib
import random


#定义叶节点
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.parent = None
        self.value = value
        self.hash = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()

    def getValue(self,value):
        self.value = value
        self.hash = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()
        return self.hash

#定义Merkle_Tree:
class Merkle_Tree:
    def __init__(self,ls):
        self.leaves = ls
        self.root = None
    #根据叶节点创建merkle树
    def create_tree(self): 
        level_nodes = []
        for i in self.leaves:
            level_nodes.append(i)
        while len(level_nodes) != 1:
            temp_nodes = []
            for i in range(0, len(level_nodes), 2):
                node_left = level_nodes[i]
                if i+1 < len(level_nodes):
                    node_right = level_nodes[i+1]
                else:
                    temp_nodes.append(level_nodes[i])
                    break

                parentValue = node_left.hash + node_right.hash
                parent = Node(parentValue)
                parent.hash = hashlib.sha256(('0x01'+parentValue).encode('utf-8')).hexdigest()
                node_left.parent = parent
                node_right.parent = parent
                parent.left = node_left
                parent.right = node_right
                temp_nodes.append(parent)
            level_nodes = temp_nodes
        self.root = level_nodes[0]
    #获取根节点的值
    def getRoot(self):
        if self.root is not None:
            return str(self.root.hash)
        else:
            return ""
    #Proof
    def getProof(self, index):
        result = self.getRoot()
        B = ""
        if len(self.leaves) > 0:
            node = self.leaves[int(index)]
        else:
            return ""
        p = node.parent
        while p is not None:
            if p.left is None:
                B = "1" + p.right.hash
            else:
                B = "0" + p.left.hash
            node = p
            p = p.parent
            result = result + " " + B
        return result
    #check inclusion
    def check_inclusion(self, value, Hash):
        arr_hash = Hash.split()
        hash_node = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()
        if arr_hash[1][0] == '0':
            p_calc = hashlib.sha256((arr_hash[1][1:] + hash_node).encode('utf-8')).hexdigest()
        elif arr_hash[1][0] == '1':
            p_calc = hashlib.sha256((hash_node + arr_hash[1][1:]).encode('utf-8')).hexdigest()
        for i in range(2, len(arr_hash)):
            hash_node = p_calc
            if arr_hash[i][0] == '0':
                p_calc = hashlib.sha256((arr_hash[i][1:] + hash_node).encode('utf-8')).hexdigest()
            elif arr_hash[i][0] == '1':
                p_calc = hashlib.sha256((hash_node + arr_hash[i][1:]).encode('utf-8')).hexdigest()
        if p_calc == arr_hash[0]:
            return True
        else:
            return False

#主函数
def main():
    #生成10w块信息
    ls = []
    for i in range(100000):
        ls.append(Node(''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789',5))))
    merkleTree=Merkle_Tree(ls)
    #创建树
    merkleTree.create_tree()
    print("Root: ",merkleTree.getRoot())
    print("Proof: ",merkleTree.getProof(5))
    value = 'abcde'
    Hash= "d71dc32fa2cd95be60b32dbb3e63009fa8064407ee19f457c92a09a5ff841a8a 13e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d 12e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6"
    print("Check inclusion: ")
    print("  value = ", value)
    print("  Hash = ", Hash)
    print("  Result: ",merkleTree.check_inclusion(value, Hash))

if __name__ == "__main__":
    main()
          
