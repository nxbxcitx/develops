import logging
import sqlite3
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def extraer(ruta):
    return pd.read_csv(ruta)


def transformar(df):
    df = df.dropna(subset=["id_venta", "monto"])
    df = df.drop_duplicates(subset="id_venta").copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["monto"] = df["monto"].astype(float)
    hoy = pd.Timestamp.today().normalize()
    return df[(df["monto"] > 0) & (df["fecha"] <= hoy)]


def cargar(df, ruta_db):
    with sqlite3.connect(ruta_db) as con:
        df.to_sql("ventas", con, if_exists="replace", index=False)


if __name__ == "__main__":
    crudo = extraer("data/ventas.csv")
    limpio = transformar(crudo)
    cargar(limpio, "ventas.db")
    log.info("Filas leidas: %d | cargadas: %d | descartadas: %d",
             len(crudo), len(limpio), len(crudo) - len(limpio))