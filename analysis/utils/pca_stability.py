# analysis/utils/pca_stability.py

def stabilize_pca_axes(df):

    df = df.copy()

    # Anchor Axis 1 to Luke Skywalker
    luke = df.loc[df["character"] == "Luke Skywalker"]

    if not luke.empty and luke["ideology_axis_1"].iloc[0] < 0:
        df["ideology_axis_1"] *= -1

    # Anchor Axis 2 to Darth Vader
    vader = df.loc[df["character"] == "Darth Vader"]

    if not vader.empty and vader["ideology_axis_2"].iloc[0] < 0:
        df["ideology_axis_2"] *= -1

    return df