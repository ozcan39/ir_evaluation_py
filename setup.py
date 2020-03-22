import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ir_evaluation_py",
    version="1.0.0",
    author="Veli Özcan Budak",
    author_email="veliozcanbudak@gmail.com",
    description="This library was created in order to evaluate the effectiveness of any kind of algorithm used in IR systems and analyze how well they perform.",
    keywords='information retrieval effectiveness evaluation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ozcan39/ir_evaluation_py",
    packages=setuptools.find_packages(),
    package_data={'ir_evaluation': ['datasets/data/*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)