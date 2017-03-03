# gingkopaper2markdown
A helper script to download markdown export from a academic paper on
gingkoapp.com.
The script exports column 5 as-is, and grabs the title and yaml
header data from column 1, the abstract from column 2.
It outputs a markdown file for further processing with pandoc.

## Usage

Clone the repository:
```bash
$ git clone git@github.com:pycnic/gingkopaper2markdown.git
$ cd gingkopaper2markdown
```

Install into current environment:
```bash
$ python setup.py install
```

Show command options:
```bash
$ gingkopaper2markdown --help
```

Configure gingkoapp username and password:
```bash
$ cp .gingkopaper2markdown.rc ~/.config/.gingkopaper2markdown
```

Edit ``~/.config/.gingkopaper2markdown`` accordingly.


## Development

Clone the repository:
```bash
$ git clone git@github.com:pycnic/gingkopaper2markdown.git
$ cd gingkopaper2markdown
```

Set up the conda environment:
```bash
$ conda env create
$ source activate gingkopaper2markdown
```
