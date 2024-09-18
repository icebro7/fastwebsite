from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import shutil
import logging

# 导入你自己的爬虫程序类
from app.copyweb.main import HtmlDownloader

router = APIRouter()


# 定义请求体的模型
class UrlRequest(BaseModel):
    url: str


# 路由1：接收URL并启动爬虫下载网页及资源文件
@router.post("/crawl-url", summary="爬虫模块")
async def crawl_url(request: UrlRequest, background_tasks: BackgroundTasks):
    url = request.url
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # 确保 URL 是合法的并带有协议头
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url

    downloader = HtmlDownloader()

    # 启动异步爬虫任务
    domain_name = await downloader.save_html_and_resources(url)
    download_link = f"/api/v1/copy/download/{domain_name}"

    logging.info(f"Crawling started for URL: {url}")

    return {"message": "Crawling started, you will be notified once done.", "download_link": download_link}


# 路由2：根据保存的文件夹路径下载压缩文件
@router.get("/download/{domain_name}", summary="下载压缩文件")
async def download_file(domain_name: str, background_tasks: BackgroundTasks):
    base_dir = os.path.join('app', 'copyweb', 'saved_page')
    save_dir = os.path.join(base_dir, domain_name)

    if not os.path.exists(save_dir):
        raise HTTPException(status_code=404, detail="Folder not found")

    # 生成压缩文件的路径
    zip_filename = f"{domain_name}.zip"
    zip_filepath = os.path.join(base_dir, zip_filename)

    try:
        # 创建压缩文件
        shutil.make_archive(os.path.splitext(zip_filepath)[0], 'zip', save_dir)

        if os.path.exists(zip_filepath):
            logging.info(f"File created at {zip_filepath}")
        else:
            logging.error(f"Failed to create file at {zip_filepath}")
    except Exception as e:
        logging.error(f"Error creating zip archive: {e}")
        raise HTTPException(status_code=500, detail="Error creating zip archive")

    response = FileResponse(zip_filepath, media_type="application/zip", filename=zip_filename)

    # 在后台任务中删除文件夹和压缩文件
    def cleanup():
        try:
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
                logging.info(f"Deleted folder: {save_dir}")
            if os.path.exists(zip_filepath):
                os.remove(zip_filepath)
                logging.info(f"Deleted zip file: {zip_filepath}")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    background_tasks.add_task(cleanup)

    logging.info(f"Zip file created and ready for download: {zip_filepath}")

    return response
