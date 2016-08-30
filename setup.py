from setuptools import setup
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name='wsappy',
    version='0.1.0',
    description='A bit more higher level of asyncio websocket server',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],
    author='Oleg Krasnikov',
    author_email='a.insolite@gmail.com',
    url='https://github.com/insolite/wsappy',
    download_url='https://github.com/insolite/wsappy',
    packages=['wsappy'],
    include_package_data=True,
    install_requires=requirements,
)
