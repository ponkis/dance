from setuptools import setup, find_packages

setup(
    name="dance",
    version="1.0",
    description="A Python app that displays a looping GIF and plays music according to BPM.",
    author="ponkiss",
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'pyautogui',
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'dance = dance:main',
        ],
    },
)
