import xml.etree.ElementTree as ET
from pathlib import Path
import shutil

def carregar_filtro(arquivo, manual_valores):
    """Carrega valores de filtro de arquivo ou lista manual."""
    if arquivo:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return [linha.strip() for linha in f if linha.strip()]
        except Exception as e:
            print(f"Erro ao carregar arquivo de filtro: {e}")
            return []
    # Caso não tenha arquivo, retorna lista manual limpa e sem vazios
    return [v.strip() for v in manual_valores if v.strip()]

def extrair_valor_xml(xml_path, campo):
    """Extrai o valor do campo do XML conforme tipo do filtro."""
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        if campo == "nNF":
            el = root.find('.//nfe:nNF', namespaces=ns)
        elif campo == "CNPJ":
            el = root.find('.//nfe:dest/nfe:CNPJ', namespaces=ns)
        elif campo == "xNome":
            el = root.find('.//nfe:dest/nfe:xNome', namespaces=ns)
        else:
            return None
        return el.text if el is not None else None
    except ET.ParseError:
        print(f"Erro ao analisar XML: {xml_path}")
        return None

def mover_arquivos(pasta_origem, pasta_destino, valores_filtro, tipo_filtro, logger):
    """Move arquivos XML que tenham valor do filtro na lista."""
    cont = 0
    origem = Path(pasta_origem)
    destino = Path(pasta_destino)

    # Garantir que pasta destino existe
    destino.mkdir(parents=True, exist_ok=True)

    for xml_file in origem.glob("*.xml"):
        valor = extrair_valor_xml(xml_file, tipo_filtro)
        if valor and valor in valores_filtro:
            destino_path = destino / xml_file.name
            try:
                shutil.move(str(xml_file), str(destino_path))
                logger(f"Movido {xml_file.name} (valor: {valor})")
                cont += 1
            except Exception as e:
                logger(f"Erro ao mover {xml_file.name}: {e}")
        else:
            logger(f"Ignorado {xml_file.name} (valor: {valor})")
    return cont
