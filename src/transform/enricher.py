import pandas as pd


def add_yoy_growth(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["pais", "anio", "mes"])
    df["arribos_ant"] = df.groupby(["pais", "mes"])["arribos"].shift(1)
    mask = df["arribos_ant"] > 0
    df.loc[mask, "crecimiento_yoy"] = (
        (df.loc[mask, "arribos"] - df.loc[mask, "arribos_ant"])
        / df.loc[mask, "arribos_ant"] * 100
    ).round(2)
    df = df.drop(columns=["arribos_ant"])
    return df


def seasonal_index(df: pd.DataFrame) -> pd.DataFrame:
    monthly_avg = df.groupby("mes")["arribos"].mean()
    global_avg = df["arribos"].mean()
    if global_avg == 0:
        return pd.DataFrame({"mes": range(1, 13), "indice_estacional": [0] * 12})
    idx = (monthly_avg / global_avg * 100).round(1)
    return idx.reset_index().rename(columns={"arribos": "indice_estacional"})


def market_share(df: pd.DataFrame) -> pd.DataFrame:
    annual = df.groupby(["pais", "anio"])["arribos"].sum().reset_index()
    total = annual.groupby("anio")["arribos"].transform("sum")
    annual["participacion_pct"] = (annual["arribos"] / total * 100).round(2)
    return annual.sort_values(["anio", "participacion_pct"], ascending=[True, False])


def covid_impact(df: pd.DataFrame) -> pd.DataFrame:
    pre = df[df["anio"].isin([2018, 2019])].groupby("pais")["arribos"].mean()
    post = df[df["anio"] == 2020].groupby("pais")["arribos"].sum()

    compare = pd.DataFrame({
        "promedio_2018_2019": pre,
        "total_2020": post,
    }).dropna()

    mask = compare["promedio_2018_2019"] > 0
    compare.loc[mask, "caida_pct"] = (
        (compare.loc[mask, "total_2020"] - compare.loc[mask, "promedio_2018_2019"])
        / compare.loc[mask, "promedio_2018_2019"] * 100
    ).round(1)

    return compare.reset_index().sort_values("caida_pct")


def recovery_index(df: pd.DataFrame, base_year: int = 2019) -> pd.DataFrame:
    base = df[df["anio"] == base_year].groupby("mes")["arribos"].sum()
    results = []
    for anio in sorted(df["anio"].unique()):
        if anio <= base_year:
            continue
        current = df[df["anio"] == anio].groupby("mes")["arribos"].sum()
        for mes in range(1, 13):
            b = base.get(mes, 0)
            c = current.get(mes, 0)
            recovery = (c / b * 100) if b > 0 else 0
            results.append({
                "anio": anio,
                "mes": mes,
                "recuperacion_pct": round(recovery, 1),
            })
    return pd.DataFrame(results)
