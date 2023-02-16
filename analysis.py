import pandas as pd
import webScrapping


def combineMatchingIndexAndCompetitiveIndex():
    dfCompetitveness = pd.read_excel('Jobs.xlsx', sheet_name='Jobs')
    dfMatching = pd.read_excel('matchIndex.xlsx', sheet_name='Sheet1')

    newdf = pd.merge(dfCompetitveness, dfMatching, on=[
                     "JobID"])
    newdf.drop(columns=["Unnamed: 0", "Openings",
               "Applicants"], inplace=True)
    newdf.to_excel('final.xlsx', sheet_name='Final')
