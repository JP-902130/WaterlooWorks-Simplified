import pandas as pd
import webScrapping


def combine():
    dfCompetitveness = pd.read_excel('Jobs.xlsx', sheet_name='Jobs')
    dfMyRating = pd.read_excel('myRating.xlsx', sheet_name='Jobs')
    dfMyRating.drop(columns=["Openings", "Applicants",
                    "Competitive Index"], inplace=True)
    newdf = pd.merge(dfCompetitveness, dfMyRating, on=[
                     "IDs", "Titles", "Companies"])
    newdf.drop(columns=["Unnamed: 0_y", "Unnamed: 0_x"], inplace=True)
    newdf.to_excel('final.xlsx', sheet_name='Final')
