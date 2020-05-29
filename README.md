# YSTAFDB

YSTAFDB creates turtle files of the istances of data based on an ontology. The turtle files are needed for the BONSAI knowledge graph. 

The turtle files generated are stored in the BONSAI [rdf repository](https://github.com/BONSAMURAIS/rdf).

Currently generates the following:

* Activity types, flow objects, locations and flows for YSTAFDB v1.0.

## Installation

### with package managers [pip or conda]

Installable via `pip`
### manual

Call `python setup.py install` inside the repository:

```
git clone git@github.com:BONSAMURAIS/ystafdb.git
cd ystafdb
pipenv install
pipenv shell
python setup.py install
```


### Download Base Data
Before using the extraction tool, the base ystafdb data must be downloaded, and placed in the correct folder.
The data can be downloaded [here](https://www.sciencebase.gov/catalog/file/get/5b9a7c28e4b0d966b485d915?f=__disk__0f%2F58%2Fa7%2F0f58a74db669ee5418f36a698bc85781e867e0ab) as a zip file.
Extract the zip file and move relevant files to the ystafdb/data folder.
Currently the following files should be moved to the data folder:

- `material_names.csv`
- `subsystems.csv`
- `flows.csv`
- `publications.csv`
- `reference_spaces.csv`
- `reference_materials.csv`
- `reference_timeframes.csv`

All other files can be disregarded.


## Usage

### As a command line tool

If the package is correctly installed, you can use the command line tool `ystafdb-cli` to produce the rdfs as follows:

```
mkdir output
ystafdb-cli regenerate output
```

This will put inside the `output` directory the following contents:

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