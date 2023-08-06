# DateVersioning

![Python package](https://github.com/EinarArnason/DateVersioning/workflows/Python%20package/badge.svg)

## The What

This is a python module to generate a git commit date based version. The first two digits represent the year, as in 20 means the year 2020 and 21 the year 2021 and so on. The middle three digits represent the day of the year ranging from 001 to 366. The last six digits represent the time of date in 24 hour format (hhmmss).

## The Why

For continuous release software, it is more user friendly to be able to read out from the version how old it is. So the user can make a decision to check up on updates based on that.

## The How

Install from PyPi:

```bash
pip install DateVersioning
```

Usage:

In a directory containing a git repository

```bash
python -m DateVersioning
```

Specify a location of a git repository

```bash
python -m DateVersioning directory="/path/to/repo"
```

## The Who

Einar Arnason  
<https://github.com/EinarArnason/>  
<https://www.linkedin.com/in/einararnason/>
