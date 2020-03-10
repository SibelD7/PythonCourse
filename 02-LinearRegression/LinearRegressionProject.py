import wbdata
import pandas
import numpy

from LinearRegression import linearRegression

class LinearRegressionProject(object):

    def getRawData(self, sSaveFile):
        aCountries = [ oCountry["id"] for oCountry in wbdata.get_country(incomelevel = "LMY", display = False) ]
        mIndicators = {
            "NY.GDP.PCAP.PP.CD": "GDP per capita (current US$)",
            "SH.DYN.MORT":       "Mortality rate, under-5 (per 1,000 live births)",
            "SG.GEN.PARL.ZS":    "Proportion of seats held by women in national parliaments (%)"
        }
        oData = wbdata.get_dataframe(mIndicators, country = aCountries, convert_date = True)
        oData.to_csv(sSaveFile)

    def processRawData(self, sInputCsv, sOutputCsv):
        oData = pandas.read_csv(sInputCsv)
        oData = oData.loc[oData["date"] == "2014-01-01"]
        oData["GDP per capita (current US$)"] = oData["GDP per capita (current US$)"] / 1000
        oData = oData.drop(["country", "date"], axis = 1)
        oData.to_csv(sOutputCsv)

    def regressionAnalysis(self, sDatasetCsv):
        aRegEst, aCovMat, aStdErr, aTStats = linearRegression(sDatasetCsv)
        print(f"Regression Estimates: {aRegEst}")
        print(f"   Covariance Matrix: {aCovMat}")
        print(f"     Standard Errors: {aStdErr}")
        print(f"        T-Statistics: {aTStats}")


if __name__ == "__main__":
    app = LinearRegressionProject()
    app.getRawData("intermediate.csv")
    app.processRawData("intermediate.csv", "dataset.csv")
    app.regressionAnalysis("dataset.csv")
