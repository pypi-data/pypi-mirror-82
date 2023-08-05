from setuptools import setup

setup(
    name='keract-nightly',
    version='5.1',
    description='Keract - Tensorflow Keras Activations and Gradients',
    author='Philippe Remy',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=['keract'],
    python_requires='>=3',
    install_requires=[
        'numpy>=1.18.5',
    ]
)
