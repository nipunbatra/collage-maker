from setuptools import setup, find_packages

setup(
    name="collage-maker",
    version="2.1.0",
    description="A Python tool for creating beautiful photo collages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nipun",
    url="https://github.com/nipunbatra/collage-maker",
    py_modules=["collage_maker"],
    install_requires=[
        "Pillow>=10.0.0",
        "click>=8.1.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "collage-maker=collage_maker:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    python_requires=">=3.7",
)