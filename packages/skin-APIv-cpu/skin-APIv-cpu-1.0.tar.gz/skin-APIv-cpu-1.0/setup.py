
from setuptools import find_packages, setup

setup(
    name = 'skin-APIv-cpu',
    version = '1.0',
    description="The API for melanoma image skin level prediction (cpu Version).",
    packages= find_packages(),
    py_modules=['skinAPI'],  # pip安裝完之後,要import時的名稱
    author="Claire",
    license="LGPL"
)