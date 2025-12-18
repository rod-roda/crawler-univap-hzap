import requests, re
from urllib.parse import unquote
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def parse_date(date_str: str):
    for fmt in ("%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Formato de data inesperado: {date_str}")

def format_comunicados(data):
    resp = []

    hoje = datetime.today().date()

    for comunicado in data:
        time_str = comunicado[5].replace(" 00:00:00", "")
        time = parse_date(time_str)
        if time == hoje:
            resp.append({
                "comunicado": comunicado[1],
                "data": time_str
            })
    return resp

def call_api():
    BASE = "https://portal.univap.br"

    session = requests.Session()
    session.headers.update({
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/127.0.0.0 Safari/537.36"),
        "Accept": "*/*",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    login_url = f"{BASE}/AOnline/web/loginsm"
    login_data = {
        "origem": "form-aluno",
        "url_origem": "/AOnline/AOnline/avisos/T016D.tp",
        "username": os.getenv("UNIVAP_USERNAME"),
        "password": os.getenv("UNIVAP_PASSWORD"),
    }
    login_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": BASE,
        "Referer": f"{BASE}/AOnline/AOnline/avisos/T016D.tp",
    }

    r = session.post(login_url, data=login_data, headers=login_headers)
    r.raise_for_status()

    if(not(r.status_code == 200)):
        return {'status': False, 'message': 'Erro na requisição', 'step': 'login'}
    
    xsrf_js = session.get(f"{BASE}/AOnline/XSRFScript", headers={
        "Referer": f"{BASE}/AOnline/AOnline/avisos/T016D.tp",
        "Origin": BASE,
    })
    xsrf_js.raise_for_status()

    if(not(xsrf_js.status_code == 200)):
        return {'status': False, 'message': 'Erro na requisição', 'step': 'Cronos Token JS'}
    
    m = re.search(r'Techne\.cronos_xsrf_token\s*=\s*"([^"]+)"', xsrf_js.text)
    if not m:
        return {'status': False, 'message': 'cronos_xsrf_token no XSRFScript não encontrado', 'step': 'Cronos Token JS'}
    cronos_token = unquote(m.group(1))

    mk = re.search(r'Techne\.cronos_xsrf_token_key\s*=\s*"([^"]+)"', xsrf_js.text)
    xsrf_header_name = mk.group(1) if mk else "cronos_xsrf_token"

    ajax_url = f"{BASE}/AOnline/AOnline/avisos/T016D.ajax"
    ajax_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": BASE,
        "Referer": f"{BASE}/AOnline/AOnline/avisos/T016D.tp",
        "X-Requested-With": "XMLHttpRequest",
        xsrf_header_name: cronos_token,
    }
    ajax_data = {"_id": "grpAvisosApenas"}

    resp = session.post(ajax_url, data=ajax_data, headers=ajax_headers)
    if(not(resp.status_code == 200)):
        return {'status': False, 'message': 'Erro na requisição', 'step': 'AJAX Avisos'}
    return {'status': True, 'response': resp.json()}

router = APIRouter(prefix="/crawler_univap", tags=['crawler_univap'])
@router.get("/", status_code=status.HTTP_200_OK)
def get_comunicados_today(request: Request):
    auth = request.headers.get("Authorization")
    api_key = os.getenv("API_KEY")
    if auth != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    ret = call_api()
    if ret.get('status'):
        return JSONResponse(content={"status": True, "comunicados": format_comunicados(ret['response']['data']['records'])})
    raise HTTPException(status_code=500, detail=ret.get("msg", "Erro interno"))

#https://portal.univap.br/AOnline/XSRFScript
#https://portal.univap.br/AOnline/AOnline/avisos/T016D.ajax