# %%
import pandas as pd
import plotly.express as px


# %%
covid19 = pd.read_csv("covid.csv")


# %%
covid19.head(5)


# %%
covid19.columns


# %%
covid19.rename(columns={"Country/Region": "Country"}, inplace=True)
covid19.rename(str.lower, axis="columns", inplace=True)


# %%
covid19 = covid19.drop(
    columns=["confirmed last week", "1 week change", "1 week % increase"]
)


# %%
covid19.dtypes


# %%
covid19.columns


# %%
covid19.info()


# %%
round(covid19.describe(), 2)


# %%
covid19.confirmed.sum()


# %% [markdown]
# Total 16 million cases were registered in this dataset.

# %%
covid19.columns


# %%
covid19.iloc[:, -1].unique()


# %% [markdown]
# #### 0. Confirmed cases in the Top 5 countries

# %%
confirmed_case = (
    covid19[["who region", "country", "confirmed"]]
    .sort_values(by="confirmed", ascending=False)
    .head(10)
)

confirmed_case

# %%
px.pie(
    confirmed_case,
    names="country",
    values="confirmed",
    color="who region",
    title="Confirmed Cases(Top 10)",
)


# %% [markdown]
# - More than 50% confirmed cases from the America continent
# - In Asia India is the only country in top 3 position.
# - Confirmed covid cases are high from these three countries(US, Brazil, and India).

# %% [markdown]
# #### 1.1 Active cases in Top 5 countries

# %%
active_case = (
    covid19[["country", "active"]].sort_values(by="active", ascending=False).head(5)
)
active_case

# %%
px.pie(active_case, names="country", values="active", title="Active cases")


# %% [markdown]
# We can see here the top 5 countries that having highest covid cases are United States, Brazil, India, United Kingdom, Russia. Comparitively other countries US is more than 5 times heavily affected by covid-19.

# %% [markdown]
# #### 1.2 Top 5 countries covid-19 death rates

# %%
death_rate = (
    covid19[["country", "who region", "deaths"]]
    .sort_values(by="deaths", ascending=False)
    .head(5)
)
death_rate

# %%
px.bar(data_frame=death_rate, x="deaths", y="country", color="country")


# %%
fig = px.pie(
    data_frame=death_rate, names="country", values="deaths", title="Death Cases"
)
fig.show()

# %% [markdown]
# Because of a highly active cases in United States country, so the death rate is also high.But surprisingly Brazil is occupies 25% of the death cases, when compared to active cases only just 12% occupied in the active cases chart.

# %% [markdown]
# #### 1.2.1 Least death rate countries with region

# %%
covid19[["country", "deaths", "who region"]].sort_values(by="deaths").head(5)


# %% [markdown]
# #### 1.3 Top recovered country or region

# %%
recovery = (
    covid19[["country", "recovered"]]
    .sort_values(by="recovered", ascending=False)
    .head()
)
recovery

# %%
px.bar(data_frame=recovery, x="recovered", y="country", color="country")


# %%
px.pie(recovery, names="country", values="recovered", title="Recovered Cases")


# %% [markdown]
# Almost every country in the world fighting hard against the Corona virus that's why the Recovery rate is good in every countries.

# %%
covid19[covid19.country == "India"].sort_values(by="active")


# %% [markdown]
# #### 2. Total cases in the top 5 regions:

# %%
covid19.columns


# %%
regions_ard = (
    covid19.groupby("who region")[["active", "recovered", "deaths"]]
    .sum()
    .sort_values(by="active", ascending=False)
)
regions_ard = regions_ard.reset_index()
regions_ard["totalcases"] = (
    regions_ard.active + regions_ard.recovered + regions_ard.deaths
)
regions_ard

# %%
px.bar(
    regions_ard,
    x=["active", "recovered", "deaths"],
    y="who region",
    labels={"who region": "Region", "value": "Count"},
)

# %% [markdown]
# Highly populated countries like India, Russia and Middle East countries are in the Asia region not that much infected by Covid-19 compared to America region. America region was almost near the 9 million count.

# %% [markdown]
# #### 3. which region's countries are mostly affected?

# %%
country_in_region = (
    covid19.groupby(["who region"])[["country"]]
    .count()
    .sort_values(["country"], ascending=False)
)

country_in_region

# %%
px.pie(
    country_in_region,
    title="Total countries in region",
    names=country_in_region.index,
    values="country",
    hole=0.5,
)

# %% [markdown]
# Totally 56 countries in Europe region and 48 countries in Africa region was affected by corona virus. This is almost half of the countries in the world.

# %% [markdown]
# #### 4. Total new cases in top 5 countries

# %%
covid19.columns


# %%
new_ard = (
    covid19.groupby(["country"])[
        [
            "new cases",
            "new deaths",
            "new recovered",
        ]
    ]
    .sum()
    .sort_values(by="new cases", ascending=False)
)
new_ard = new_ard.reset_index().head(10)
new_ard

# %%
new_ard["total_new_cases"] = (
    new_ard["new cases"] + new_ard["new recovered"] + new_ard["new deaths"]
)
new_ard

# %%
px.bar(new_ard, x=["new cases", "new deaths", "new recovered"], y="country")


# %% [markdown]
# - New cases are highly popping in the United States, India and Brazil.
# - 70% of new cases are popping in these 3 countries.

# %%
px.pie(new_ard, names="country", values="total_new_cases")


# %%
covid19.head()


# %% [markdown]
# #### 5. 100 cases visualization

# %%
covid19.columns


# %%
covid19 = covid19.rename(
    columns={
        "deaths / 100 cases": "case100_deaths",
        "recovered / 100 cases": "case100_recovered",
        "deaths / 100 recovered": "rec100_deaths",
    }
)

covid19.head()

# %%
covid19.columns


# %%
case100 = (
    covid19.groupby(["who region"])[["case100_deaths", "case100_recovered"]]
    .mean()
    .sort_values(by="who region")
    .reset_index()
)
case100

# %%
px.bar(
    case100,
    x="who region",
    y=["case100_deaths", "case100_recovered"],
    color="who region",
)

# %%
px.pie(case100, names="who region", values="case100_recovered")


# %% [markdown]
# Recovery rate per 100 case almost same in all regions.

# %%
px.pie(case100, names="who region", values="case100_deaths")


# %% [markdown]
# But the Death Rate per 100 case high in the Europe and East Mediterranean Region. So this plot concludes 1% to 5% of people will die who were infected by Corona virus.

# %% [markdown]
# ### Summary:
#
# 1. Where is **China**'s data? (Mystery)
# #
# 2. The top 5 countries that having highest covid cases are United States, Brazil, India, United Kingdom, Russia. Comparitively other countries US is more than 5 times heavily affected by covid-19.
# - More than 50% confirmed cases from the America continent
# - In Asia India is the only country in top 3 confirmed cases.
# - Because of a highly active cases in United States country, so the death rate is also high.
# - Highly populated countries like India, Russia and Middle East countries are in the Asia region not that much infected by Covid-19 compared to America region.
# - America region was almost near the 9 million count.
# - New cases are highly popping in the United States, India and Brazil.
# - 70% of new cases are popping in these 3 countries.
# #
# 3. Totally 56 countries in Europe region and 48 countries in Africa region was affected by corona virus. This is almost half of the countries in the world.
# #
# 4. the Death Rate per 100 case high in the Europe and East Mediterranean Region. So this plot concludes 1% to 5% of people will die who were infected by Corona virus.
# #
# 5. Almost every country in the world fighting hard against the Corona virus that's why the Recovery rate is good in every countries.
