import os
import logging
import aiohttp
import aiofiles
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import asyncio
import chardet


class HtmlDownloader:
    def __init__(self, max_concurrent_requests=10):
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def get_domain_name(self, url):
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.split('.')[1]  # 获取主域名
        return domain_name

    async def download_file(self, session, url, folder):
        async with self.semaphore:
            try:
                local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
                async with session.get(url) as response:
                    response.raise_for_status()
                    async with aiofiles.open(local_filename, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            await f.write(chunk)
                logging.info(f"Downloaded: {url} -> {local_filename}")
                return local_filename
            except aiohttp.ClientError as e:
                logging.error(f"Failed to download {url}: {e}")
                return None

    async def save_html(self, soup, output_folder):
        try:
            html_filename = os.path.join(output_folder, "index.html")
            async with aiofiles.open(html_filename, 'w', encoding='utf-8') as f:
                await f.write(soup.prettify())
            logging.info(f"HTML saved: {html_filename}")
        except Exception as e:
            logging.error(f"Failed to save HTML: {e}")

    async def download_resources(self, session, soup, base_url, css_folder, js_folder, img_folder):
        tasks = []

        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(base_url, link['href'])
            tasks.append(self.download_file(session, css_url, css_folder))

        for script in soup.find_all('script', src=True):
            js_url = urljoin(base_url, script['src'])
            tasks.append(self.download_file(session, js_url, js_folder))

        for img in soup.find_all('img', src=True):
            img_url = urljoin(base_url, img['src'])
            tasks.append(self.download_file(session, img_url, img_folder))

        # 使用 gather 并发执行任务，并处理失败的任务
        await asyncio.gather(*tasks, return_exceptions=True)

    async def save_html_and_resources(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                # 获取原始字节数据
                content = await response.read()
                # 使用 chardet 检测编码
                detected_encoding = chardet.detect(content)['encoding']
                # 使用检测到的编码解码内容
                text = content.decode(detected_encoding)
                soup = BeautifulSoup(text, 'html.parser')

                domain_name = await self.get_domain_name(url)
                save_dir = os.path.join('app', 'copyweb', 'saved_page', domain_name)
                os.makedirs(save_dir, exist_ok=True)

                css_folder = os.path.join(save_dir, 'css')
                js_folder = os.path.join(save_dir, 'js')
                img_folder = os.path.join(save_dir, 'images')
                os.makedirs(css_folder, exist_ok=True)
                os.makedirs(js_folder, exist_ok=True)
                os.makedirs(img_folder, exist_ok=True)

                await self.download_resources(session, soup, url, css_folder, js_folder, img_folder)

                # 修改 HTML 文件中的资源路径
                for link in soup.find_all('link', rel='stylesheet'):
                    link['href'] = os.path.join('css', os.path.basename(urlparse(link['href']).path))

                for script in soup.find_all('script', src=True):
                    script['src'] = os.path.join('js', os.path.basename(urlparse(script['src']).path))

                for img in soup.find_all('img', src=True):
                    img['src'] = os.path.join('images', os.path.basename(urlparse(img['src']).path))

                await self.save_html(soup, save_dir)

                return domain_name
