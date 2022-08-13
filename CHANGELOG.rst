=========
Changelog
=========

Version 0.0.2
=============
Updated to work with changes to KNMI API.

Data that can be requested via the API has remained the same, but there are several noteworthy changes

* API endpoints have been updated.
* Station names are not included in the dataframes by default anymore, instead only the station number is given. The parser still outputs a dataframe with station names and respective numbers, so they can still be linked.
* The metadata provided by the KNMI for several variables and API endpoints has changed, sometimes dramatically. Unfortunately the documentation on the `KNMI website <https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script>`_ does not fully reflect what the API provides anymore.
* The previous version of the parser was fairly flexible, but the new version unfortunately relies on parsing hard-coded 'blocks' of information, because of some small inconsistencies. Unfortunately this also means minor changes to the formatting by KNMI will break the functionality of the parser again (but not data download).

If somehow the parser or other functionalities stop working, don't hesitate to open an issue on `GitHub <https://github.com/barthoekstra/knmy>`_.

Version 0.0.1
=============
Initial release.