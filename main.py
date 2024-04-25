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

    def addNewBlock(self):
        self.prepareDataToIncludeInNewBlock()
        newBlock = self.generateNewBlock()
        newBlock = self.proofOfWorkForBlock(newBlock, difficulty=4)
        if newBlock:
            self._chain.append(newBlock)
            self._pendingData.removeDuplicates(self._dataToIncludeInNewBlock, dataCompareFunction)
            self._dataToIncludeInNewBlock = []
