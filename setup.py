from setuptools import setup
from pip.req import parse_requirements

import wsappy as package


install_reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name=package.__name__,
    version=package.__version__,
    packages=[package.__name__],
    url='https://github.com/insolite/{}'.format(package.__name__),
    author='Oleg Krasnikov',
    author_email='a.insolite@gmail.com',
    description='A bit more higher level of asyncio websocket server',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],
    install_requires=requirements,
)
