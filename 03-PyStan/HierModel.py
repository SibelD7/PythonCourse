#!/usr/bin/env python3

*Model with Diffuse Prior*

import pandas
import pystan

DATAFILE_NAME = "trend2.csv"
STAN_MODEL = """
data {
    int<lower=0> N_COUNTRIES;
    int<lower=0> N_SAMPLES;
    int<lower=1, upper=N_COUNTRIES> country[N_SAMPLES];
    vector[N_SAMPLES] gini_net;
    vector[N_SAMPLES] rgdpl;
    vector[N_SAMPLES] church2;
}

parameters {
    vector[N_COUNTRIES] a;
    real beta_1;
    real beta_2;
    real mu_a;
    real<lower=0,upper=100> sigma_a;
    real<lower=0,upper=100> sigma_y;
}

transformed parameters {
    vector[N_SAMPLES] y_hat;
    for (i in 1:N_SAMPLES)
        y_hat[i] = a[country[i]] + gini_net[i] * beta_1 + rgdpl[i] * beta_2;
}

model {
    sigma_a ~ uniform(0, 100);
    a ~ normal(mu_a, sigma_a);
    beta_1 ~ cauchy(0,25);
    beta_2 ~ normal(0,1);
    sigma_y ~ uniform(0, 100);
    church2 ~ normal(y_hat, sigma_y);
}
"""

oDataFrame = pandas.read_csv(DATAFILE_NAME).drop("cc", axis = "columns").dropna()
oDataFrame.country = oDataFrame.country.str.strip()

aUniqueCountries = oDataFrame.country.unique()
mCountryLookup = { aData[0]: aData[1] for aData in zip(aUniqueCountries, range(aUniqueCountries.size)) }
oDataFrame.country = oDataFrame.country.replace(mCountryLookup)

mStanData = {
    "N_COUNTRIES": aUniqueCountries.size,
    "N_SAMPLES":   oDataFrame.count()[0],
    "country":     (oDataFrame.country + 1).values, # Stan is 1-indexed
    "gini_net":    oDataFrame.gini_net.values,
    "rgdpl":       oDataFrame.rgdpl.values,
    "church2":     oDataFrame.church2.values
}
oStanModel = pystan.StanModel(model_code = STAN_MODEL)
oFit = oStanModel.sampling(data = mStanData, iter = 1000, chains = 4)
print(oFit)
oFit.plot()



*Model with highly informative Prior*

import pandas
import pystan

DATAFILE_NAME = "trend2.csv"
STAN_MODEL = """
data {
    int<lower=0> N_COUNTRIES;
    int<lower=0> N_SAMPLES;
    int<lower=1, upper=N_COUNTRIES> country[N_SAMPLES];
    vector[N_SAMPLES] gini_net;
    vector[N_SAMPLES] rgdpl;
    vector[N_SAMPLES] church2;
}

parameters {
    vector[N_COUNTRIES] a;
    real beta_1;
    real beta_2;
    real mu_a;
    real<lower=0,upper=100> sigma_a;
    real<lower=0,upper=100> sigma_y;
}

transformed parameters {
    vector[N_SAMPLES] y_hat;
    for (i in 1:N_SAMPLES)
        y_hat[i] = a[country[i]] + gini_net[i] * beta_1 + rgdpl[i] * beta_2;
}

model {
    sigma_a ~ uniform(0, 100);
    a ~ normal(mu_a, sigma_a);
    beta_1 ~ normal(0,1);
    beta_2 ~ normal(0,1);
    sigma_y ~ uniform(0, 100);
    church2 ~ normal(y_hat, sigma_y);
}
"""

oDataFrame = pandas.read_csv(DATAFILE_NAME).drop("cc", axis = "columns").dropna()
oDataFrame.country = oDataFrame.country.str.strip()

aUniqueCountries = oDataFrame.country.unique()
mCountryLookup = { aData[0]: aData[1] for aData in zip(aUniqueCountries, range(aUniqueCountries.size)) }
oDataFrame.country = oDataFrame.country.replace(mCountryLookup)

mStanData = {
    "N_COUNTRIES": aUniqueCountries.size,
    "N_SAMPLES":   oDataFrame.count()[0],
    "country":     (oDataFrame.country + 1).values, # Stan is 1-indexed
    "gini_net":    oDataFrame.gini_net.values,
    "rgdpl":       oDataFrame.rgdpl.values,
    "church2":     oDataFrame.church2.values
}
oStanModel = pystan.StanModel(model_code = STAN_MODEL)
oFit = oStanModel.sampling(data = mStanData, iter = 1000, chains = 4)
print(oFit)
oFit.plot()