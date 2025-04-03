import base64
import requests
from app.config import envs, logger

B2_API_KEY_ID = envs.B2_API_KEY_ID
B2_API_KEY = envs.B2_API_KEY
B2_BUCKET_ID = envs.B2_BUCKET_ID


async def authorize_b2():
    try:
        logger.info("🔔 B2 인증 요청 시작")
        url = "https://api.backblaze.com/b2api/v3/b2_authorize_account"
        headers = {
            "Authorization": (
                "Basic "
                + base64.b64encode(
                    f"{B2_API_KEY_ID}:{B2_API_KEY}".encode()
                ).decode()
            )
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info("✅ B2 인증 성공")
        return response.json()

    except Exception as e:
        logger.error(f"❌ 인증 실패: {e}")
        return None


async def get_upload_url_b2():
    try:
        logger.info("🔔 B2 업로드 URL 요청 시작")
        authorize_result = await authorize_b2()
        if not authorize_result:
            logger.error("❌ 인증 결과가 없습니다. 업로드 URL 요청 중단")
            return None

        api_url = authorize_result["apiInfo"]["storageApi"]["apiUrl"]
        token = authorize_result["authorizationToken"]
        url = f"{api_url}/b2api/v3/b2_get_upload_url?bucketId={B2_BUCKET_ID}"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info("✅ B2 업로드 URL 요청 성공")
        return response.json()

    except Exception as e:
        logger.error(f"❌ 전송 URL 호출 실패: {e}")
        return None
