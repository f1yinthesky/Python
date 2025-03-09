from typing import List, Set
import asyncio
from queue import SimpleQueue
from datetime import datetime
from urllib import parse
import time

def NormalizeUrl(url:str) -> str:
    return parse.urlparse(url)._replace(fragment="").geturl().lower()

def getUrlDomain(url:str) -> str:
    return parse.urlparse(NormalizeUrl(url)).netloc

async def genUrls(url: str) -> List[str]:
    await asyncio.sleep(2)
    path = url.split("/")
    reply_urls = []
    reply_urls.append(url.lower())
    if len(path) < 6:
        letter = path[-1][-1]
        for i in range(4):
            new_url = url + "/" + chr(ord(letter) + i + 1)
            reply_urls.append(new_url)
            reply_urls.append(parse.urlparse(new_url)._replace(netloc="b.com").geturl())
    return reply_urls

def getUrls(url: str) -> List[str]:
    return asyncio.run(genUrls(url))

def getUrlsNew(url: str) -> List[str]:
    time.sleep(2)
    path = url.split("/")
    reply_urls = []
    reply_urls.append(url.lower())
    if len(path) < 6:
        letter = path[-1][-1]
        for i in range(4):
            new_url = url + "/" + chr(ord(letter) + i + 1)
            reply_urls.append(new_url)
            reply_urls.append(parse.urlparse(new_url)._replace(netloc="b.com").geturl())
    return reply_urls

async def genUrlsNew(url: str) -> List[str]:
    new_urls = await asyncio.to_thread(getUrlsNew, url)
    return new_urls

async def visitOneUrl(url_queue: SimpleQueue, visited_url: Set[str], domain_name:str) -> None:
    if url_queue.empty():
        return
    current_url = url_queue.get()
    print(f"{datetime.now()} url {current_url}")
    if current_url not in visited_url:
        all_urls = await genUrlsNew(current_url)
    visited_url.add(current_url)
    for url in all_urls:
        url = NormalizeUrl(url)
        if url not in visited_url and getUrlDomain(url) == domain_name:
            url_queue.put(url)


async def main():
    url_queue = SimpleQueue()
    first_url = "https://A.com#dd"
    domain_name = getUrlDomain(first_url)
    url_queue.put(NormalizeUrl(first_url))

    visited_url = set()
    while not url_queue.empty():
        all_workers = []
        for i in range(10):
            all_workers.append(visitOneUrl(url_queue, visited_url, domain_name))
        await asyncio.gather(*all_workers)



if __name__=="__main__":
    asyncio.run(main())