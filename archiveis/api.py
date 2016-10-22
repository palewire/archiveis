#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import click
import requests
from six.moves.urllib.parse import urljoin


def capture(
    target_url,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)",
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
    }

    # Send the capture request to archive.is
    data = {
        "coo": '',
        "url": target_url,
        "anyway": 1,
    }
    response = requests.post(save_url, headers=headers, data=data)

    # archive.is returns a link format timemap in the header field link
    # but if it was the first time archive.is has archived the uri-r
    # or for some other reason unknown at this time
    # this information will not be present so resort to searching the
    # returned html page
    memento_re = re.compile('"(http(?:s)?://archive\.is/(?:[0-9]{14}/(?:\b)?)?'
                            '[-a-zA-Z0-9@:%_+.~#?&/=]+)"',
                            re.IGNORECASE | re.MULTILINE)
    mementos = memento_re.findall(response.text)

    # the url to the memento is the first element in the list
    return mementos[0]


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
