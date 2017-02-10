from setuptools import setup

setup(name='python_cipres',
    version='0.1',
    description='cipres rest client',
    url='',
    author='Terri Liebowitz Schwartz',
    author_email='terri@sdsc.edu',
    license='',
    packages=['python_cipres'],
    install_requires=[
        "pymysql == 0.5",
        "requests == 2.5.3",
		"pystache == 0.5.3",
    ],
    scripts=[
		"bin/tooltest.py",
		"bin/cipresjob.py",
    ],

    zip_safe=False)
