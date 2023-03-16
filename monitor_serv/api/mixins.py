import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from http import HTTPStatus
from pprint import pprint

import requests
from django.http import JsonResponse


class PromQueryMixin:
   pass