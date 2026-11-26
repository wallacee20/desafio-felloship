
import logging
import sys

from etl.pipeline import executar_pipeline


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    try:

        resultado = executar_pipeline()

        logging.info("RESUMO FINAL DA EXECUÇÃO: %s", resultado)

    except Exception:

        logging.exception("Falha na execução do pipeline ETL")

        sys.exit(1)


if __name__ == "__main__":
    main()
