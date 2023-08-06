# magnelPy

magnelPy is a Python toolbox for the ea14 research group of Ghent University

## Getting Started

### Prerequisites

[Python 3.6](https://www.anaconda.com/download/) or later; and

The following Python libraries:

```sh
numpy==1.15.0
pandas==0.23.3
scipy==1.1.0
```

### Installation

#### pip

pip is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python ](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

magnelPy uses Python3. 

1.	If you are using Windows with Python version 3.3 or higher, use the [Python Launcher for Windows](https://docs.python.org/3/using/windows.html?highlight=shebang#python-launcher-for-windows) to use `pip` with Python version 3:
    ```sh
    pip install magnelPy
    ```
2.	If your system has a `python3` command (standard on Unix-like systems), install with:
    ```sh
    python3 -m pip install magnelPy
    ```
3.	You can also just use the `python` command directly, but this will use the _current_ version of Python in your environment:
    ```sh
    python -m pip install magnelPy
    ```

### Usage

Using the help(.) functionality to explore the package functionalities is recommended.

Application steps:
1. pip install magnelPy (e.g. within conda environment)
2. explore magnelPy functionality
	$\gt\gt\gt$ import magnelPy
	$\gt\gt\gt$ help(magnelPy)
3. [example] explore magnelPy.SFE.FireCurve functionality
	$\gt\gt\gt$ import magnelPy.SFE as sfe
	$\gt\gt\gt$ help(sfe.FireCurve)

Command line functionality:
- SAFIR run
```sh
python -c "import magnelPy.SAFIRshell as x; x.runSAFIR()"
```
- concrete slab temperature calculation EN1992-1-2:2004, ISO 834
```sh
python -c "import magnelPy.SFE as x; x.EC_concreteSlab_ISO834()"
```

## Authors

* **Ranjit Chaudhary** - *ranjit.chaudhary@ugent.be*
* **Balsa Jovanovic** - *balsa.jovanovic@ugent.be*
* **Thomas Thienpont** - *thomas.thienpont@UGent.be*
* **Ruben Van Coile** - *ruben.vancoile@ugent.be*

## Past contributors and acknowledgement
* **Wouter Botte** - *wouter.botte@ugent.be*
* **Nicky Reybrouck** - *nicky.reybrouck@ugent.be*


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details - under the additional requirement of acknowledging the magnelPy development community.
