from setuptools import setup, find_packages

setup(
    name='owngpt',
    version='0.0.1',
    author='Abhay Chourasiya',
    author_email='Abhaychourasiya945@gmail.com',
    description='It is a Offline No-Realtime Assistant and Online-Realtime Assistant',
    url='https://github.com/Abhay06102003/OwnGPT',  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_cors',
        'pydantic',
        'aiohttp',
        'beautifulsoup4',
        'googlesearch-python',
        'langchain',
        'torch',
        'fastapi',
        'uvicorn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        "console_scripts": [
            "owngpt=OwnGPT.app:main",
        ],
    },
    python_requires='>=3.10',
)