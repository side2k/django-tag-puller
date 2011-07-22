from setuptools import setup, find_packages

setup(
    name='tag-puller',
    version='0.3b',
    description='Tag puller plugin for django',
    author='outsider',
    author_email='outsider@atvc.ru',
    url='http://www.atvc.ru',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
