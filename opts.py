
import sys
import logging

from luma.core import cmdline, error


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s - %(message)s'
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    print("FOTOMETRIA POR EMISSAO POR CAPTURA DE IMAGENS   FIRMWARE VER 1.0.7" )
    print("Analises dos elementos por processamento de imagem")
    print("Elementos de analises")
    print("Sodio (Na), Calcio (C), Potassio (K) e Litio (Li)")
    print("Aguarde, iniciando ......") 

    # create device
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)

    return device
