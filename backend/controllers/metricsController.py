from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPBearer, OAuth2PasswordBearer)
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path
import json
import subprocess
import sys

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/", response_model=dict)
def get_metrics():
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    metrics_path = BASE_DIR  / 'data' / 'processed' / 'metrics.json'
    etl_script_path = BASE_DIR / 'data' / 'etl.py'

    if not metrics_path.exists():
        print("Arquivo metrics.json não encontrado. Executando o ETL...")

        try:
            result = subprocess.run(
                [sys.executable, str(etl_script_path)],
                capture_output=True,
                text=True,
                check=True
            )
            print("ETL executado com sucesso:", result.stdout)
        except subprocess.CalledProcessError as e:           
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Falha ao executar o script ETL.",
            )
        except FileNotFoundError:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"O script etl.py não foi encontrado no caminho: {etl_script_path}",
            )

    try:
        with open(metrics_path, 'r', encoding='utf-8') as f:
            metrics_data = json.load(f)
        return metrics_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao ler o arquivo JSON: {str(e)}",
        )