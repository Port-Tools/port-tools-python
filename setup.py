from setuptools import find_packages, setup
setup(
    name='port.tools-sdk',
    packages=find_packages(),
    version='1.0.0',
    description='Port.Tools Python SDK',
    author_email='hung.caovu@gmail.com',
    author='Port.Tools',
    url='https://github.com/selwin/python-user-agents',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['README.md']},
    install_requires=[],
    classifiers=[
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

