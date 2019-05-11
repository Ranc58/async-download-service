import logging
import os

import asyncio

from aiohttp import web
import aiofiles

from config import CONFIG


async def get_archive_process(data_path):
    archive_process = await asyncio.create_subprocess_shell(
        f'zip -r - {CONFIG["photos_path"]}/{data_path}/',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return archive_process


async def archive_handle(request):
    response = web.StreamResponse()
    archive_hash = request.match_info.get('archive_hash')
    is_path_exist = os.path.exists(f'{CONFIG["photos_path"]}/{archive_hash}')
    if not is_path_exist:
        return web.Response(
            text='Архив не существует или был удален',
            status=404
        )
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_hash}.zip"'

    await response.prepare(request)

    archive_process = await get_archive_process(archive_hash)

    try:
        while True:
            chunk_archive = await archive_process.stdout.readline()
            logging.debug('Sending archive chunk ...')
            if not chunk_archive:
                break
            await response.write(chunk_archive)
            await asyncio.sleep(CONFIG['response_timeout'])
    except asyncio.CancelledError:
        archive_process.kill()
        raise
    finally:
        response.force_close()
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    if CONFIG['logging']:
        logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    host = CONFIG['host']
    port = CONFIG['port']
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive_handle),
    ])
    web.run_app(app, host=host, port=port)
