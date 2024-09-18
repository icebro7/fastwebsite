from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import logging

app = FastAPI()
router = APIRouter()

# 视频路径和项目文件路径（可根据需求修改）
VIDEO_PATH = "deploy/sample_video"
PROJECT_PATH = "app/copyweb/send_zip"

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 路由1：提供视频文件的播放功能
@router.get("/show-video", summary="播放视频文件")
async def stream_video(video_name: str):
    video_file_path = os.path.join(VIDEO_PATH, video_name)

    if not os.path.exists(video_file_path):
        logger.error(f"Video not found: {video_file_path}")
        raise HTTPException(status_code=404, detail="Video not found")

    if not video_file_path.endswith(".mp4"):
        logger.error(f"Invalid video file type: {video_file_path}")
        raise HTTPException(status_code=400, detail="Invalid video file type")

    logger.info(f"Streaming video: {video_file_path}")
    return FileResponse(video_file_path, media_type="video/mp4")


# 路由2：提供项目文件的下载
@router.get("/download-rar", summary="下载项目文件")
async def download_project_file(project_name: str, background_tasks: BackgroundTasks):
    project_file_path = os.path.join(PROJECT_PATH, project_name)

    if not os.path.exists(project_file_path):
        logger.error(f"Project not found: {project_file_path}")
        raise HTTPException(status_code=404, detail="Project not found")

    if not project_file_path.endswith(".rar"):
        logger.error(f"Invalid project file type: {project_file_path}")
        raise HTTPException(status_code=400, detail="Invalid project file type")

    logger.info(f"Downloading project file: {project_file_path}")
    return FileResponse(project_file_path, media_type="application/rar", filename=f"{project_name}.rar")
