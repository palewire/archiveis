#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import logging
import re
import requests
from six.moves.urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)


def send_request(target, user_agent, proxies, data=None):
    """Send HTTP requests and handle the response"""
    # Configure the request headers
    headers = {
        'User-Agent': user_agent,
        "host": "archive.fo",
    }
    # Configure request arguments
    request_kwargs = dict(
        timeout=120,
        allow_redirects=True,
        headers=headers,
    )
    if proxies:
        request_kwargs['proxies'] = proxies
    # Send request
    if data is None:
        # this is a GET request
        logger.debug("Requesting (GET) {}".format(target))
        response = requests.get(target, **request_kwargs)
        response.raise_for_status()
    else:
        # this is a POST request
        request_kwargs["data"] = data
        logger.debug("Requesting (POST) {}".format(target))
        response = requests.post(target, **request_kwargs)
        response.raise_for_status()
    return response


def capture(
    target_url,
    user_agent="archiveis (https://github.com/pastpages/archiveis)",
    proxies={},
    screenshot=False,
    zip_file=False,
):
    """
    Archives the provided URL using archive.is

    Returns the URL where the capture is stored.
    """
    # Put together the URL that will save our request
    memento = None
    domain = "http://archive.fo"
    save_url = urljoin(domain, "/submit/")

    # Request a unique identifier for our activity
    id_request = domain + "/"
    # Send request
    response = send_request(id_request, user_agent, proxies)

    # It will need to be parsed from the homepage response headers
    try:
        unique_id = response.text.split('name="submitid', 1)[1].split('value="', 1)[1].split('"', 1)[0]
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

    # Send request
    response = send_request(save_url, user_agent, proxies, data)

    # There are a couple ways the header can come back
    if 'Refresh' in response.headers:
        memento = str(response.headers['Refresh']).split(';url=')[1]
        logger.debug("Memento from Refresh header: {}".format(memento))
    elif 'Location' in response.headers:
        memento = response.headers['Location']
        logger.debug("Memento from Location header: {}".format(memento))
    else:
        logger.debug("Memento not found in response headers. Inspecting history.")
        for i, r in enumerate(response.history):
            logger.debug("Inspecting history request #{}".format(i))
            logger.debug(r.headers)
            if 'Location' in r.headers:
                memento = r.headers['Location']
                logger.debug("Memento from the Location header of {} history response: {}".format(i+1, memento))
    # If there's nothing at this point, throw an error
    if memento is None:
        logger.error("No memento returned by archive.is")
        logger.error("Status code: {}".format(response.status_code))
        logger.error(response.headers)
        logger.error(response.text)
        raise Exception("No memento returned by archive.is")
    # else
    screenshot_response = None
    zip_response = None
    memento_id = re.sub("^https?://archive.fo/", "", memento)
    # sleep to let the page load
    if screenshot is True or zip_file is True:
        time.sleep(60)
    if screenshot is True:
        # first request
        screenshot_url = memento + '/image'
        logger.debug(screenshot_url)
        response = send_request(screenshot_url, user_agent, proxies)
        pattern = 'https?://archive.fo/'  + memento_id + '/[a-f0-9]+?/scr.png'
        print(pattern)
        match = re.search(pattern, response.text)
        if match:
            # second request
            screenshot_url = match.group(0)
            logger.debug(screenshot_url)
            response = send_request(screenshot_url, user_agent, proxies)
            screenshot_response = response.content
    if zip_file is True:
        zip_url = 'http://archive.fo/download/' + memento_id + '.zip'
        logger.debug(zip_url)
        response = send_request(zip_url, user_agent, proxies)
        zip_response = response.content
    return memento, screenshot_response, zip_response


@click.command()
@click.argument("url")
@click.option("-ua", "--user-agent", help="User-Agent header for the web request")
@click.option("-s", "--screenshot", help="Download a rendered screenshot (defaults to 'snapshot name'.png)", is_flag=True)
@click.option("-z", "--zip-file", help="Download a ZIP-file containing the webpage (defaults to 'snapshot name'.zip)", is_flag=True)
def cli(url, user_agent, screenshot, zip_file):
    """
    Archives the provided URL using archive.is.
    """
    kwargs = {}
    if user_agent:
        kwargs['user_agent'] = user_agent
    if screenshot:
        kwargs['screenshot'] = screenshot
    if zip_file:
        kwargs['zip_file'] = zip_file
    archive_url, screenshot_response, zip_response = capture(url, **kwargs)
    click.echo(archive_url)
    if screenshot or zip_file:
        snapshot_name = re.sub("^https?://archive.fo/", "", archive_url)
        if screenshot:
            if screenshot_response is not None:
                filename = snapshot_name + '.png'
                with open(filename, 'wb') as outfile:
                    outfile.write(screenshot_response)
                click.echo('Screenshot saved')
            else:
                logger.error("No screenshot returned by archive.is")
        if zip_file:
            if zip_response is not None:
                filename = snapshot_name + '.zip'
                with open(filename, 'wb') as outfile:
                    outfile.write(zip_response)
                click.echo('ZIP-file saved')
            else:
                logger.error("No ZIP file returned by archive.is")


if __name__ == "__main__":
    cli()
