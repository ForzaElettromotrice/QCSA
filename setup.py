from setuptools import find_packages, setup

setup(
    name = 'QCSA',
    packages = find_packages(include = ['QCSA']),
    version = '0.1.0',
    description = 'Boh, da scrivere',
    author = 'ForzaElettromotrice',
    author_email = 'mingardi.federico@gmail.com',
    python_requires = '>=3.11',
    install_requires = ['qiskit'],
    extras_require = { },
    license_files = ['LICENSE']
)
