import time
import logging
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg2

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '데이터베이스가 사용 가능할 때까지 실행을 일시 중지하는 Django 명령어'

    def add_arguments(self, parser):
        parser.add_argument('--max_retries', type=int, default=10, help='최대 재시도 횟수')
        parser.add_argument('--retry_interval', type=int, default=1, help='재시도 간격(초)')

    def handle(self, *args, **options):
        max_retries = options['max_retries']
        retry_interval = options['retry_interval']

        self.stdout.write('PostgreSQL 데이터베이스 연결 대기 중...')
        logger.info('PostgreSQL 데이터베이스 연결 시도 시작')

        db_config = settings.DATABASES['default']
        self.stdout.write(f"데이터베이스 정보: {db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}")

        for i in range(max_retries):
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                with db_conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                db_conn.close()
                self.stdout.write(self.style.SUCCESS(f'PostgreSQL 데이터베이스 연결 성공! (버전: {version})'))
                logger.info(f'PostgreSQL 데이터베이스 연결 성공 (버전: {version})')
                return
            except (OperationalError, psycopg2.OperationalError) as e:
                self.stdout.write(self.style.WARNING(
                f'데이터베이스 연결 실패. {retry_interval}초 후 다시 시도합니다... (시도 {i + 1}/{max_retries})')
                )
                logger.warning(f'데이터베이스 연결 실패: {str(e)}. 재시도 중... (시도 {i + 1}/{max_retries})')
                time.sleep(retry_interval)

        self.stdout.write(self.style.ERROR(f'{max_retries}번의 시도 후에도 PostgreSQL 데이터베이스에 연결하지 못했습니다.'))
        logger.error(f'{max_retries}번의 시도 후 데이터베이스 연결 실패')
        exit(1)