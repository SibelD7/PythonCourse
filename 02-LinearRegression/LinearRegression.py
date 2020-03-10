import pandas
import numpy

def linearRegression(sCsvPath):
    """
    Runs a linear regression on the data contained in a CSV file

    Arguments:
        sCsvPath: (string) path to the CSV file

    Returns:
        A 4-tuple, with the values in this order:
            * (numpy.array) Regression Estimates
            * (numpy.array) Variance and Covariance Matrix
            * (numpy.array) Standard Errors
            * (numpy.array) T-Statistics
    """

    # Read in the CSV and clean up the data (remove header and the garbage first column)
    oDataFrame = pandas.read_csv(sCsvPath)
    oDataFrame = oDataFrame.dropna()
    oDataFrame = oDataFrame.drop([oDataFrame.columns[0]], axis = 1)

    # Run the linear regression
    aOutcomeVar = numpy.array(oDataFrame.iloc[:, 0], ndmin = 2).T
    aCovariates = numpy.array(oDataFrame.iloc[:, 1:], ndmin = 2)
    aDependentVar = numpy.concatenate((numpy.ones((len(aOutcomeVar),1)), aCovariates), axis = 1)
    aBeta = numpy.linalg.inv(aDependentVar.T @ aDependentVar) @ aDependentVar.T @ aOutcomeVar
    aFitted = aDependentVar @ aBeta
    aResidual = aOutcomeVar - aFitted
    fSigmaSquared = (aResidual.T @ aResidual) / (len(aOutcomeVar)- len(aCovariates[1, :]) -1)
    aVarBeta = fSigmaSquared * numpy.linalg.inv(aDependentVar.T @ aDependentVar)
    aStdErrors = numpy.array([numpy.sqrt(aVarBeta[i, i]) for i in range(oDataFrame.shape[1])])
    aTStats = numpy.array([aBeta[i] / numpy.sqrt(aVarBeta[i, i]) for i in range(oDataFrame.shape[1])])

    # Done, return a nice tuple of values to play with
    return (aBeta, aVarBeta, aStdErrors, aTStats)
