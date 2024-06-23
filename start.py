import uvicorn
import os

from app.config import MCIMConfig, Aria2Config
from app.database.mongodb import init_mongodb_aioengine
from app.database._redis import init_redis_aioengine

from app import APP


mcim_config = MCIMConfig.load()
aria2_config = Aria2Config.load()

if __name__ == "__main__":
    init_mongodb_aioengine()
    init_redis_aioengine()
    if mcim_config.file_cdn:
        os.makedirs(aria2_config.modrinth_download_path, exist_ok=True)
        os.makedirs(aria2_config.curseforge_download_path, exist_ok=True)
        for i in range(256):
            os.makedirs(os.path.join(aria2_config.modrinth_download_path, format(i, '02x')), exist_ok=True)
            os.makedirs(os.path.join(aria2_config.curseforge_download_path, format(i, '02x')), exist_ok=True)
    uvicorn.run(APP, host=mcim_config.host, port=mcim_config.port)