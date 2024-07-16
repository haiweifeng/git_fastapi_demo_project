#!/usr/bin/env python
# -*- coding:utf-8 -*-
from fastapi import APIRouter
router = APIRouter()

from .role_view import *
from .user_view import *
