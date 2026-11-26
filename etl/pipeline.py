
import logging

from etl.extract import executar_extracao
from etl.transform import executar_transformacao
from etl.load import executar_carga


def executar_pipeline():

    logging.info("========== INICIANDO PIPELINE ETL ==========")

    # 1. Extração
    logging.info("ETAPA 1/3 - EXTRAÇÃO")

    metricas_extracao = executar_extracao()

    logging.info(
        "Extração concluída: %s",
        metricas_extracao
    )

    # 2. Transformação
    logging.info("ETAPA 2/3 - TRANSFORMAÇÃO")

    metricas_transformacao = executar_transformacao()

    logging.info(
        "Transformação concluída: %s",
        metricas_transformacao
    )

    # 3. Carga
    logging.info("ETAPA 3/3 - CARGA")

    metricas_carga = executar_carga()

    logging.info(
        "Carga concluída: %s",
        metricas_carga
    )

    # Resultado final
    resultado = {
        "extracao": metricas_extracao,
        "transformacao": metricas_transformacao,
        "carga": metricas_carga
    }

    logging.info("========== PIPELINE FINALIZADO ========== ")

    return resultado
