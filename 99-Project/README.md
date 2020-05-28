# Project - Spam Detection with Logistic Regression, using TensorFlow

## How To Run

Due to the size of the datasets involved, this project requires an extremely
powerful computer to run. Recommended specs are:

* 32 GB RAM (Optimistic Estimate)
* nVidia GPU with CUDA cores

You will need the following Python modules:

* nltk
* numpy
* tensorflow

NOTE: This project has never been run with the full Enron dataset because
I simply do not have access to a computer powerful enough to handle the size
of this dataset. The theory has been proven with a smaller synthetic dataset.
The synthetic dataset is available in the `synthetic` directory

### Step 1: Downloading the Enron Spam Dataset

1. Download the 6 files (Enron1 through Enron6) linked in this page:
http://nlp.cs.aueb.gr/software_and_datasets/Enron-Spam/index.html
2. When extracted, each of them produce one folder (enron1 through enron6).
Each of these folders have two subfolders: `spam` and `ham`. Merge them all
under one `enron` folder so that you have `enron/{spam,ham}/*.txt`

### Step 2: Producing the Feature Vector and Feature Matrices

These emails need to be processed into a feature matrix. In addition, the
feature vector itself needs to be saved so that arbitrary emails can be
later tested.

Open a python console and run:

    from ProcessData import DataProcessor

    oDP = DataProcessor()
    oDP.processAllMails("enron")
    oDP.buildFeatureVector()
    oDP.saveFeatureVector("features.txt")
    oDP.buildFeatureMatrix("spam.csv", "ham.csv")

### Step 3: Training the Model

Training the model is the most time-consuming part of the process. Open a
Python console and run:

    from Regression import LogisticRegressionPredictor

    oLRP = LogisticRegressionPredictor()
    oLRP.loadData()
    oLRP.trainModel("model.hd5")

### Step 4: Testing an Email

Testing an email is simple and fast. To test an email, use the following code:

    from Regression import LogisticRegressionPredictor
    from ProcessData import DataProcessor

    sMail = """Subject: Nigerian Prince Needs Help
    ... some obviously spammy text ..."""

    oDP = DataProcessor()
    oDP.loadFeatureVector("features.txt")
    aMailVector = oDP.buildAdhocMailVector(sMail)

    oLRP = LogisticRegressionPredictor()
    oLRP.predictMail("model.hd5", sMail)

The return is in the form of [spamminess, hamminess]
