from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import platform

# class CustomInstallCommand(install):
#     """Customized setuptools install command to run a command after installation."""
#     def run(self):
#         install.run(self)  # Call the standard install process
#         # Run your custom command only if the OS is Linux
#         if platform.system() == 'Linux':  # Check if the OS is Linux
#             subprocess.call(['curl -fsSL https://ollama.com/install.sh | sh'])  # Replace with your command
#             subprocess.call(['ollama run llama3.2'])
#         else:
#             raise RuntimeError("This package requires Ollama to be installed from the web on non-Linux systems. (After Installation run 'ollama run llama3.2')")

setup(
    name='owngpt',
    version='0.0.1',
    author='Abhay Chourasiya',
    author_email='Abhaychourasiya945@gmail.com',
    description='It is a Offline No-Realtime Assistant and Online-Realtime Assistant',
    url='https://github.com/Abhay06102003/OwnGPT',
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
        'ollama',
        'langchain-chroma',
        'langchain-huggingface',
        'sentence-transformers'
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