import json
import random
import time
import uuid

from datetime import datetime
from hashlib import sha256


class Blockchain(object):
    class DATA_TYPE:
        TRANSACTION_CODE = 100
        TRANSACTION = {"code": TRANSACTION_CODE, "description": "transaction"}

    def __init__(self):
        self._chain = []
        self._pendingData = ThreadSafeList()
        self._dataToIncludeInNewBlock = []

    def prepareDataToIncludeInNewBlock(self):
        self._dataToIncludeInNewBlock = self._pendingData.getChunk()
        # self._dataToIncludeInNewBlock = self._pendingData[:min(2,len(self._pendingData))]

    def addNewBlock(self):
        def dataCompareFunction(data1, data2):
            if data1["uuid"] == data2["uuid"]:
                return True
            return False

        self.prepareDataToIncludeInNewBlock()
        newBlock = self.generateNewBlock()
        newBlock = self.proofOfWorkForBlock(newBlock, difficulty=4)

        # If newBlock == None then calculating PoW must be
        # interrupted by some external action, for example
        # arrival of block mined by other node.
        if newBlock:
            self._chain.append(newBlock)
            # BEGIN: Remove from _pendingData everything which is in _dataToIncludeInNewBlock
            self._pendingData.removeDuplicates(self._dataToIncludeInNewBlock, dataCompareFunction)
            # END
            self._dataToIncludeInNewBlock = []

            return True
        else:
            return False

    def acceptNewBlock(self, block):
        # In future version add some code here
        # to add to this blockchain structure
        # block mined by other node

        # Verify block
        # If verification is positive then add new block
        # Remove from pendingData data present in new block
        pass

    def computeHashForData(self, data):
        return computeMerkleTree(data)

    def generateNewBlock(self):
        data = self._dataToIncludeInNewBlock
        merkleTree = self.computeHashForData(data)

        if len(self._chain) > 0:
            previousBlock = self._chain[-1]
            previousBlockHash = previousBlock["header"]["blockHash"]
        else:
            genesisString = 'Genesis string'
            genesisStringBytes = genesisString.encode('utf-8')
            previousBlockHash = sha256(genesisStringBytes).hexdigest()

        block = {
            "header": {
                "previousBlockHash": previousBlockHash,
                "timestamp": datetime.utcnow().isoformat(),
                "dataMainHash": merkleTree[-1][0],
                "difficulty": None,
                "nonce": None
            },
            "data": data,
            "metadata": {
                "merkleTree": merkleTree
            }
        }

        return block

    def proofOfWorkForBlock(self, block, difficulty):
        leadingZeros = "0" * difficulty

        start = time.time()
        block["header"]["difficulty"] = difficulty

        print("Start mining")
        while True:
            block["header"]["nonce"] = format(random.getrandbits(64), "x")
            dataString = json.dumps(block, sort_keys=True)
            dataBytes = dataString.encode('utf-8')

            hash = sha256(dataBytes).hexdigest()

            if hash.startswith(leadingZeros):
                block["header"]["blockHash"] = hash
                end = time.time()
                block["header"]["mineTime"] = end - start
                break

        return block

    def addNewTransaction(self, sender, recipient, amount, document, signatureOfDocument):
        data = {
            "uuid": uuid.uuid4().hex,
            "dataType": self.DATA_TYPE.TRANSACTION,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "document": document,
            "sendersSignature": signatureOfDocument
        }

        self._pendingData.push(data)

    def hashBlock(self, block):
        blockAsBytes = json.dumps(block, sort_keys=True).encode('utf-8')
        return sha256(blockAsBytes).hexdigest()

    def saveBlockchain(self):
        data = {
            "chain": self._chain,
            "pendingData": self._pendingData._list,
            "dataToIncludeInNewBlock": self._dataToIncludeInNewBlock
        }

        with open("blockchain.txt", "w") as fileData:
            json.dump(data, fileData)

    def loadBlockchain(self):
        with open("blockchain.txt") as fileData:
            data = json.load(fileData)

            self._chain = data["chain"]
            self._pendingData._list = data["pendingData"]
            self._dataToIncludeInNewBlock = data["dataToIncludeInNewBlock"]

def computeMerkleTree(data):
    dataAsString = []
    dataHashes = []

    for d in data:
        jsonAsString = json.dumps(d, sort_keys=True)
        dataAsString.append(jsonAsString)

        dataAsBytes = jsonAsString.encode('utf-8')
        dataHashes.append(sha256(dataAsBytes).hexdigest())

    #merkleTree = [dataAsString, dataHashes]
    merkleTree = [dataHashes]

    while len(merkleTree[-1])>1:
        size = len(merkleTree[-1])
        i = 0
        hashes = []
        while i<size:
            h1 = merkleTree[-1][i]
            i += 1
            if i==size:
                hashes.append(h1)
                break
            h2 = merkleTree[-1][i]
            i += 1

            h = sha256(h1.encode('utf-8')+h2.encode('utf-8')).hexdigest()

            hashes.append(h)

        merkleTree.append(hashes)

    return merkleTree



"""# Class `ThreadSafeList`"""

from threading import Lock

# Custom class wrapping a list
# in order to make it thread safe.
class ThreadSafeList():
    def __init__(self):
        self._list = []
        self._lock = Lock()

    def push(self, value):
        with self._lock:
            self._list.append(value)

    def pop(self):
        with self._lock:
            return self._list.pop()

    def get(self, index):
        with self._lock:
            return self._list[index]

    def length(self):
        with self._lock:
            return len(self._list)

    def getChunk(self, size=None):
        with self._lock:
            if size is None:
                n = len(self._list)
            else:
                n = min(size,len(self._list))
            chunk = self._list[:n]
            return chunk

    def removeDuplicates(self, data, compareFunction):
        with self._lock:
            listLocal = []
            dd = []

            for e in range(len(self._list)):
                present = False

                for d in range(len(data)):
                    if (d not in dd) and (compareFunction(self._list[e], data[d])):
                        present = True
                        dd.append(d)
                        break

                if present == False:
                    listLocal.append(self._list[e])

            self._list = listLocal
