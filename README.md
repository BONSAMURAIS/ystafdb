# YSTAFDB

YSTAFDB creates turtle files of the istances of data based on an ontology. The turtle files are needed for the BONSAI knowledge graph. 

The turtle files generated are stored in the BONSAI [rdf repository](https://github.com/BONSAMURAIS/rdf).

Currently generates the following:

* Activity types, flow objects, locations and flows for YSTAFDB v1.0.

## Installation

### with package managers [pip or conda]

Installable via `pip`
### manual

Clone git repo
```
$ git clone git@github.com:BONSAMURAIS/ystafdb.git
```

Enter cloned repo
```
$ cd ystafdb
```
##### Download Base Data 
Before progressing the installation, the base ystafdb data must be downloaded, and placed in a folder of your choosing, inside the repo.
The data can be downloaded [here](https://www.sciencebase.gov/catalog/file/get/5b9a7c28e4b0d966b485d915?f=__disk__0f%2F58%2Fa7%2F0f58a74db669ee5418f36a698bc85781e867e0ab) as a zip file.
Extract the zip file and move relevant files to a folder. As an example, the data can be placed under `/ystafdb/data/`.
The following ystafdb files are mandatory to have in the folder:
- `material_names.csv`
- `subsystems.csv`
- `flows.csv`
- `publications.csv`
- `reference_spaces.csv`
- `reference_materials.csv`
- `reference_timeframes.csv`

##### Create env and install dependencies
Either 1) create new virtualenv and enter shell or 2) enter already existing virtualenv and install dependencies
##### Option 1)
```
$ pipenv install
$ pipenv shell
```

##### Option 2)
```
$ source path/to/environment/bin/activate
$ pip install -r requirements.txt
```

Now install package
```
$ python setup.py install
```


## Usage

### As a command line tool

If the package is correctly installed, you can use the command line tool `ystafdb-cli` to produce the rdfs as follows:

```
$ ystafdb-cli -i <input/dir> -o  <output/dir>
```

Where `<input/dir>` is the location of the ystafdb csv files, and `<output/dir>` is the directory where the output triples graphs will be placed. 
The `<output/dir>` directory will have the following content:

```
output
├── activitytype
│   └── ystafdb
│       └── ystafdb.ttl
├── flowobject
│   └── ystafdb
│       └── ystafdb.ttl
├── location
│   └── ystafdb
│       └── ystafdb.ttl
├── foaf
│   └── ystafdb
│       └── ystafdb.ttl
└── prov
|   └── ystafdb
|       └── ystafdb.ttl
└── flow
    └── ystafdb
        └── huse
            └── huse.ttl

```


## Contributing
All contributions should be via pull request, do not edit this package directly! We actually use it for stuff.