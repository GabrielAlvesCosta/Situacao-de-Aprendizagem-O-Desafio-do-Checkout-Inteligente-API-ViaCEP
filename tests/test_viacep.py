import pytest
import requests

@pytest.fixture(scope='session')
def api_client():

    with requests.Session() as session:
        yield session 


@pytest.fixture(scope='function')
def base_url():

    return "https://viacep.com.br/ws/"




def test_cep_valido_retorna_200_e_dados(api_client, base_url):

    cep = "01001000"
    url = f"{base_url}{cep}/json/"
    
    response = api_client.get(url)
    dados = response.json()
    
    assert response.status_code == 200
    assert "erro" not in dados
    assert dados["cep"] == "01001-000"
    assert dados["logradouro"] == "Praça da Sé"
    assert dados["bairro"] == "Sé"
    assert dados["localidade"] == "São Paulo"


def test_cep_inexistente_retorna_flag_de_erro(api_client, base_url):

    cep = "99999999"
    url = f"{base_url}{cep}/json/"
    
    response = api_client.get(url)
    dados = response.json()
    
    assert response.status_code == 200
    assert dados.get("erro") == "true"


def test_cep_formato_invalido_retorna_400(api_client, base_url):

    cep_invalido = "123"
    url = f"{base_url}{cep_invalido}/json/"
    
    response = api_client.get(url)
    
    assert response.status_code == 400

def test_cep_com_hifen_na_url_retorna_200(api_client, base_url):

    cep_com_hifen = "01001-000"
    url = f"{base_url}{cep_com_hifen}/json/"
    
    response = api_client.get(url)
    dados = response.json()
    

    assert response.status_code == 200
    assert "erro" not in dados
    assert dados["cep"] == "01001-000"


def test_estrutura_do_json_retornado_schema(api_client, base_url):

    cep = "01001000"
    url = f"{base_url}{cep}/json/"
    
    response = api_client.get(url)
    dados = response.json()
    
    chaves_esperadas = [
        "cep", "logradouro", "complemento", "bairro", 
        "localidade", "uf", "ibge", "gia", "ddd", "siafi"
    ]
    
    assert response.status_code == 200

    for chave in chaves_esperadas:
        assert chave in dados, f"A chave obrigatória '{chave}' sumiu do retorno da API!"


def test_tempo_de_resposta_da_api(api_client, base_url):

    cep = "01001000"
    url = f"{base_url}{cep}/json/"
    
    response = api_client.get(url)
    tempo_resposta = response.elapsed.total_seconds()
    
    assert tempo_resposta < 2.0, f"A API demorou muito! Tempo: {tempo_resposta}s"