from hashlib import sha256
from datetime import datetime
import json
import random
import time
import uuid



class Blockchain(object):
    class DATA_TYPE:
        TRANSACTION_CODE = 100
        TRANSACTION = {"code": TRANSACTION_CODE, "description": "transaction description", }

    def __init__(self):
        self._chain = []
        self._pendingData = []
        self._dataToIncludeInNewBlock = []

    def prepareDataToIncludeInNewBlock(self):
        self._dataToIncludeInNewBlock = self._pendingData.getChunk()
        newBlock =

    def addNewBlock(self):
        def dataCompareFunction(data1, data2):
            if data1["uuid"] != data2["uuid"]:
                return True
            else:
                return False

        self.prepareDataToIncludeInNewBlock()
        newBlock = self.generateNewBlock()
        newBlock = self.proofOfWorkForBlock(newBlock, difficulty=4)
        if newBlock:
            self._chain.append(newBlock)
            self._pendingData.removeDuplicates(self._dataToIncludeInNewBlock, dataCompareFunction)
            self._dataToIncludeInNewBlock = []

            return True
        else:
            return False

        # Funkcja która w przyszłych wersjach będzie akceptować bloki wykopane przez inne osoby
        def acceptNewBlock(self, block):
            pass

        def computeHashForData(self, data) :
            return computeMarkleTree(data)

        def generateNewBlock(self):
            data = self._dataToIncludeInNewBlock
            merkleTree = self.computeHashForData(data)

            if len(self._chain) > 0:
                prevBlock = self._chain[-1]
                prevblockHash = prevBlock["header"]["blockHash"]
            else:
                genesisString = 'Genesis Block'
                genesisStringBytes = genesisString.encode('utf-8')
                prevblockHash = sha256(genesisStringBytes).hexdigest()

            block = {
                "header": {
                    "prevblockHas": prevblockHash,
                    "timestamp": datetime.utcnow().isoformat(),
                    "dataMainHash": merkleTree[-1][0],
                    "difficulty": None,
                    "nonce": None
                },
                "data": data,
                "matadata": {
                    "merkleTree": merkleTree,
                }


            }

            return block

        def proofofWorkForBlock(self, block, difficulty):
            pass

        def addNewTransaction(self, sender, recipient, amount, document, signatureOfDocument):
            data = {
                "uuid": uuid.uuid4().hex,
                "dataType": self.DATA_TYPE.TRANSACTION,
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
                "document": document,
                "senderSignature": signatureOfDocument,
            }
            self._pendingData.push(data)

        def hashBlock(self, block):
            blockAsBytes = json.dumps(block, sort_keys=True).encode('utf-8')
            return sha256(blockAsBytes).hexdigest()

        def saveBlockBlockchain(self):
            data = {
                "chain": self._chain,
                "pendingData": self._pendingData._list,
                "dataToIncludeInNewBlock": self._dataToIncludeInNewBlock,
            }
            with open('blockchain.txt', 'w') as fileData:
                json.dump(data, fileData)

        def loadBlockBlockchain(self):
            with open('blockchain.txt', 'r') as fileData:
                data = json.load(fileData)

                self.chain = data["chain"]
                self.pendingData = data["pendingData"]
                self.dataToIncludeInNewBlock = data["dataToIncludeInNewBlock"]