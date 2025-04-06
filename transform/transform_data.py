import pandas as pd
from utils.normalize import remove_accents


def transform_cobertura_movil(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformar datos de cobertura movil
    """
    df["COD MUNICIPIO"] = df["COD MUNICIPIO"].fillna(50325)
    df = df.drop(["CABECERA MUNICIPAL", "COD CENTRO POBLADO", "CENTRO POBLADO"], axis=1)
    df["COD DEPARTAMENTO"] = df["COD DEPARTAMENTO"].astype(int)
    df["COD MUNICIPIO"] = df["COD MUNICIPIO"].astype(int)
    df["Llave"] = (
        df["COD DEPARTAMENTO"].astype(str).str.zfill(4)
        + "_"
        + df["COD MUNICIPIO"].astype(str).str.zfill(4)
    )
    df["AÑO_TRIMESTRE"] = df["AÑO"].astype(str) + "_" + df["TRIMESTRE"].astype(str)

    return df


def transform_internet_fijo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformar datos de internet_fijo sin generar SettingWithCopyWarning.
    """
    df = df.copy()

    df["MUNICIPIO"] = df["MUNICIPIO"].str.lower()
    df["MUNICIPIO"] = df["MUNICIPIO"].str.replace(r"\s+", " ", regex=True)
    df["MUNICIPIO"] = df["MUNICIPIO"].apply(remove_accents)

    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].str.lower()
    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].str.replace(r"\s+", " ", regex=True)
    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].apply(remove_accents)

    df = df[df["DEPARTAMENTO"] != "colombia"].copy()

    df.loc[df["MUNICIPIO"] == "belen de bajira", "COD_MUNICIPIO"] = 27086

    df.loc[:, "COD_DEPARTAMENTO"] = df["COD_DEPARTAMENTO"].astype(int)
    df.loc[:, "COD_MUNICIPIO"] = df["COD_MUNICIPIO"].astype(int)

    df.loc[:, "Llave"] = (
        df["COD_DEPARTAMENTO"].astype(str).str.zfill(4)
        + "_"
        + df["COD_MUNICIPIO"].astype(str).str.zfill(4)
    )

    df.loc[:, "AÑO_TRIMESTRE"] = df["AÑO"].astype(str) + "_" + df["TRIMESTRE"].astype(str)

    return df


def transform_revistas_indexadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformar datos de revistas indexadas
    """
    columns_to_drop = [
        "TXT_ISSN_P",
        "TXT_ISSN_E",
        "TXT_ISSN_L",
        "REG_REV_IN",
        "ID_INST_EDIT_1",
        "ID_INST_EDIT_2",
        "NME_INST_EDIT_2",
        "ID_REVISTA_P",
        "ID_INST_EDIT_3",
        "NME_INST_EDIT_3",
        "TIPO_INS_N4_E1",
        "TIPO_INS_N1_E2",
        "TIPO_INS_N2_E2",
        "TIPO_INS_N3_E2",
        "TIPO_INS_N4_E2",
        "TIPO_INS_N1_E3",
        "TIPO_INS_N2_E3",
        "TIPO_INS_N3_E3",
        "TIPO_INS_N4_E3",
    ]
    df = df.drop(columns=columns_to_drop, axis=1)
    df["AÑO"] = df["NRO_ANO"].astype(int)
    df.dropna(subset=["COD_DANE_REV_IN"], inplace=True)
    df["COD_MUNICIPIO"] = df["COD_DANE_REV_IN"].astype(int).astype(str).str.zfill(4)
    df["COD_DEPARTAMENTO"] = (
        df["COD_DANE_REV_IN"].astype(int).astype(str).str[:-3].str.zfill(4)
    )
    df["Llave"] = df["COD_DEPARTAMENTO"] + "_" + df["COD_MUNICIPIO"]

    return df


def transform_grupo_investigacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformar datos de grupo investigaciones
    """
    df.drop_duplicates()
    df = df.drop(
        [
            "ID_CONVOCATORIA",
            "NME_CONVOCATORIA",
            "NME_GRUPO_GR",
            "NME_REGION_GR",
            "NME_PAIS_GR",
        ],
        axis=1,
    )
    df = df.dropna(subset=["COD_DANE_GR"])
    df["FCREACION_GR"] = pd.to_datetime(df["FCREACION_GR"])
    df["COD_MUNICIPIO"] = df["COD_DANE_GR"].astype(str).str.zfill(4)

    df["COD_DEPARTAMENTO"] = df["COD_DANE_GR"].astype(str).str[:-3].str.zfill(4)
    df["Llave"] = df["COD_DEPARTAMENTO"] + "_" + df["COD_MUNICIPIO"]
    df["AÑO"] = df["FCREACION_GR"].dt.year
    df["AÑO_TRIMESTRE"] = (
        df["AÑO"].astype(str) + "_" + df["FCREACION_GR"].dt.quarter.astype(str)
    )

    return df

def filter_by_year_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtrar por rango de años de interes
    """
    return df[(df["AÑO"] >= 2015) & (df["AÑO"] <= 2022)]