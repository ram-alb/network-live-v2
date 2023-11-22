# Network Live

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

The radio network consists of its own base stations and partner operator stations. The configuration of our base stations is directly obtained from the Operations Support System (OSS), while for partner stations, it is extracted from configuration logs in various formats (xml, csv, xlsx). This project parses specific parameters from all sources and stores them in a database categorized by each Radio Access Technology technology.