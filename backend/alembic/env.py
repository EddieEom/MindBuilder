# backend/alembic/env.py

import sys
import os
from logging.config import fileConfig

# 1. 프로젝트 루트를 파이썬 경로에 추가 (절대 경로 문제 해결)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, pool
from alembic import context

# 2. 우리 설정과 모델 import
from app.core.config import settings
from app.models.base import Base
from app.models import *

# Alembic Config 객체 가져오기
config = context.config

# 로깅 설정 (기본값)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online() -> None:
    # 3. 핵심 수정: settings.sync_database_url을 직접 사용하여 엔진 생성
    print(f"Connecting to: {settings.sync_database_url}") # 연결 확인용 로그
    
    connectable = create_engine(
        settings.sync_database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()