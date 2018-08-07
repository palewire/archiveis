#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import logging
import requests
from six.moves.urllib.parse import urljoin
logger = logging.getLogger(__name__)


def capture(
    target_url,
    user_agent="archiveis (https://github.com/pastpages/archiveis)",
    proxies={}
):
    """
    Archives the provided URL using archive.is

    Returns the URL where the capture is stored.
    """
    # Put together the URL that will save our request
    domain = "http://archive.is"
    save_url = urljoin(domain, "/submit/")

    # Configure the request headers
    headers = {
        'User-Agent': user_agent,
        "host": "archive.is",
    }

    # Request a unique identifier for our activity
    logger.debug("Requesting {}".format(domain + "/"))
    get_kwargs = dict(
        timeout=120,
        allow_redirects=True,
        headers=headers,
    )
    if proxies:
        get_kwargs['proxies'] = proxies
    response = requests.get(domain + "/", **get_kwargs)
    response.raise_for_status()

    # It will need to be parsed from the homepage response headers
    html = str(response.content)
    try:
        unique_id = html.split('name="submitid', 1)[1].split('value="', 1)[1].split('"', 1)[0]
        logger.debug("Unique identifier: {}".format(unique_id))
    except IndexError:
        logger.warn("Unable to extract unique identifier from archive.is. Submitting without it.")
        unique_id = None

    # Send the capture request to archive.is with the unique id included
    data = {
        "url": target_url,
        "anyway": 1,
    }
    if unique_id:
        data.update({"submitid": unique_id})

    post_kwargs = dict(
        timeout=120,
        allow_redirects=True,
        headers=headers,
        data=data
    )
    if proxies:
        post_kwargs['proxies'] = proxies

    logger.debug("Requesting {}".format(save_url))
    response = requests.post(save_url, **post_kwargs)
    response.raise_for_status()

    # There are a couple ways the header can come back
    if 'Refresh' in response.headers:
        memento = str(response.headers['Refresh']).split(';url=')[1]
        logger.debug("Memento from Refresh header: {}".format(memento))
        return memento
    if 'Location' in response.headers:
        memento = response.headers['Location']
        logger.debug("Memento from Location header: {}".format(memento))
        return memento
    logger.debug("Memento not found in response headers. Inspecting history.")
    for i, r in enumerate(response.history):
        logger.debug("Inspecting history request #{}".format(i))
        logger.debug(r.headers)
        if 'Location' in r.headers:
            memento = r.headers['Location']
            logger.debug("Memento from the Location header of {} history response: {}".format(i+1, memento))
            return memento
    # If there's nothing at this point, throw an error
    logger.error("No memento returned by archive.is")
    logger.error("Status code: {}".format(response.status_code))
    logger.error(response.headers)
    logger.error(response.text)
    raise Exception("No memento returned by archive.is")


@click.command()
@click.argument("url")
@click.option("-ua", "--user-agent", help="User-Agent header for the web request")
def cli(url, user_agent):
    """
    Archives the provided URL using archive.is.
    """
    kwargs = {}
    if user_agent:
        kwargs['user_agent'] = user_agent
    archive_url = capture(url, **kwargs)
    click.echo(archive_url)


if __name__ == "__main__":
    cli()
