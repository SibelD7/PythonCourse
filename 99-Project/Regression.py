import numpy as np
import tensorflow as tf

class LogisticRegressionPredictor(object):
    
    def __init__(self):
        self._aTrainFeatures = None
        self._aTrainLabels = None
        self._aTestFeatures = None
        self._aTestLabels = None
        self._iNumFeatures = 0
        self._iNumLabels = 0

    def loadData(self):
        fnToNumpyArray = lambda sFileName, sDelimiter: np.genfromtxt(sFileName, delimiter = sDelimiter, dtype = None)

        print("Loading data...")
        aSpamData = fnToNumpyArray("spam.csv", ",")
        aHamData = fnToNumpyArray("ham.csv", ",")

        print("Splitting data into training and testing sets...")
        self._iNumFeatures = aSpamData.shape[1]
        self._iNumLabels = 2
        self._aTrainLabels = []
        self._aTestLabels = []

        iNumTrain = round(0.75 * len(aSpamData))
        self._aTrainFeatures = aSpamData[0:iNumTrain]
        self._aTestFeatures = aSpamData[iNumTrain:]
        iTrainSpamRecords = len(self._aTrainFeatures)
        iTestSpamRecords = len(self._aTestFeatures)
        for _ in range(0, iTrainSpamRecords):
            self._aTrainLabels.append([1, 0])
        for _ in range(0, iTestSpamRecords):
            self._aTestLabels.append([1, 0])
        
        iNumTrain = round(0.75 * len(aHamData))
        iTrainHamRecords = len(aHamData[0:iNumTrain])
        iTestHamRecords = len(aHamData[iNumTrain:])
        self._aTrainFeatures = np.concatenate((self._aTrainFeatures, aHamData[0:iNumTrain]))
        self._aTestFeatures = np.concatenate((self._aTestFeatures, aHamData[iNumTrain:]))
        for _ in range(0, iTrainHamRecords):   
            self._aTrainLabels.append([0, 1])
        for _ in range(0, iTestHamRecords):
            self._aTestLabels.append([0, 1])
        
        self._aTrainLabels = np.array(self._aTrainLabels)
        self._aTestLabels = np.array(self._aTestLabels)

    def trainModel(self, sModelPath):
        oModel = tf.keras.Sequential([
            tf.keras.layers.Dense(self._iNumLabels, input_shape = (self._iNumFeatures,), activation = "sigmoid")
        ])
        oModel.compile(optimizer = "sgd", loss = "mean_squared_error", metrics = ["accuracy"])
        oModel.fit(x = self._aTrainFeatures, y = self._aTrainLabels, shuffle = True, epochs = 27000, batch_size = 10)
        oModel.save(sModelPath)
        
        aEval = oModel.evaluate(x = self._aTestFeatures, y = self._aTestLabels)
        print("Evaluation:")
        print(aEval)
    
    def predictMail(self, sModelPath, aMailVector):
        oModel = tf.keras.models.load_model(sModelPath)
        return oModel.predict(aMailVector)
