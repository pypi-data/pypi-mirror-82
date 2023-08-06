Papermerge LimitPages Plugin/App
=================================

App/Plugin for [Papermerge DMS](https://github.com/ciur/papermerge).
Designed as Django reusable app. When used, will limit number of pages of uploaded documents to
values specified by settings.LIMITPAGES_MAX_PAGES (15 by default).

## Requirements

Depends on:

    * papermerge.core


## Installation

Install it using pip::
    
    pip install limitpages

Add app to INSTALLED_APPS in settings.py:

    INSTALLED_APP = (
    ...
    'limitpages',
    ...
    )

Add in settings.py:

    LIMITPAGES_MAX_PAGES = 13
