from distutils.core import setup

setup(
    name="glacier_lengths",
    version="0.0.1",
    description="Tools to measure glacier lengths statistically",
    url="https://github.com/erikmannerfelt/glacier_lengths.git",
    author="Erik Schytt Mannerfelt",
    author_email="mannerfelt@vaw.baug.ethz.ch",
    packages=["glacier_lengths"],
    install_requires=["shapely", "numpy"],
    extras_require={"matplotlib": ["matplotlib"]},
)
