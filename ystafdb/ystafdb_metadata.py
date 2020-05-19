from . import data_dir
from .filesystem import write_graph
from .graph_common import add_common_elements, generate_generic_graph
from .provenance_uris import get_empty_prov_graph, add_prov_meta_information
from .graph_common import NS
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, XSD, OWL
from rdflib.namespace import RDFS, DC
from rdflib import Namespace
import codecs
import csv
import re
import pkg_resources
import itertools
import pandas
import math
import os


def generate_ystafdb_metadata_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    # Get Empty Provenance Graph
    prov_graph = get_empty_prov_graph()
    prov_graph = add_prov_meta_information(prov_graph)

    # Index of Super Dataset
    ystafdb_id = 0
    dataset_counter = ystafdb_id + 1

    # publication Data
    file_path = os.path.join(data_dir, "publications.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    publications = pandas.read_csv(
        file_handler,
        header=0,
    )

    bprov_uri = "http://rdf.bonsai.uno/prov/ystafdb"
    bprov = Namespace("{}#".format(bprov_uri))
    prov = Namespace("http://www.w3.org/ns/prov#")
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    spar = Namespace("http://purl.org/spar/datacite/")

    dataset_list = []
    for i in range(0, len(publications)):
        # TODO: author info missing
        author = publications['author'][i] if type(publications['author'][i]) != float else False
        title = publications['title'][i] if type(publications['title'][i]) != float else False
        doi = publications['doi'][i] if type(publications['doi'][i]) != float else False
        notes = publications['notes'][i] if type(publications['notes'][i]) != float else False
        pub_id = publications['publication_id'][i] if type(publications['publication_id'][i]) != float else False

        node = URIRef(bprov["dataset_{}".format(pub_id + dataset_counter)])
        dataset_counter += 1
        dataset_list.append(node)
        prov_graph.add((node, RDF.type, prov.Entity))
        prov_graph.add((node, spar.hasGeneralResourceType, dtype.Dataset))
        if doi:
            prov_graph.add((node, spar.hasIdentifier, Literal(doi, datatype=XSD.string)))
        if title:
            prov_graph.add((node, DC.title, Literal(title, datatype=XSD.string)))
        if notes:
            prov_graph.add((node, RDFS.label, Literal(notes, datatype=XSD.string)))

    # Add membership to super-dataset
    super_dataset = URIRef(bprov['dataset_{}'.format(ystafdb_id)])
    for dataset in dataset_list:
        prov_graph.add((super_dataset, prov.hadMember, dataset))

    # Activity Types
    file_path = os.path.join(data_dir, "aggregate_subsystem_modules.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    processes_df = pandas.read_csv(
        file_handler,
        header=0,
    )

    activity_data = [[processes_df["aggregate_subsystem_module"][x].strip(), "A_{}".format(processes_df['aggregate_subsystem_module_id'][x])] for x in range(1, len(processes_df))]
    generate_generic_graph(
        output_base_dir,
        kind="ActivityType",
        data=sorted(activity_data),
        directory_structure=["ystafdb"],
        title="Yale Stocks and Flows Database Activity Types",
        description="ActivityType instances needed for BONSAI modelling of YSTAFDB version 1.0",
        author="BONSAI team",
        provider="Yale University",
        dataset="YSTAFDB"
    )

    # Flow Objects
    file_path = os.path.join(data_dir, "material_names.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    materials = pandas.read_csv(
        file_handler,
        header=0,
    )

    materials_data = [[materials["material_name"][x].strip(), "C_{}".format(materials['material_name_id'][x])] for x in range(0, len(materials)) if type(materials["material_name"][x]) != float]
    generate_generic_graph(
        output_base_dir,
        kind="FlowObject",
        data=materials_data,
        directory_structure=["ystafdb"],
        title="Yale Stocks and Flows Database Flow Objects",
        description="FlowObject instances needed for BONSAI modelling of YSTAFDB version 1.0",
        author="BONSAI team",
        provider="Yale University",
        dataset="YSTAFDB"
    )

    # Locations
    file_path = os.path.join(data_dir, "reference_spaces.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    locations = pandas.read_csv(
        file_handler,
        header=0,
    )

    ystafdb_location_uri = "http://rdf.bonsai.uno/location/ystafdb"
    g = add_common_elements(
        graph=Graph(),
        base_uri=ystafdb_location_uri,
        title="Custom locations for YSTAFDB",
        description="Country groupings used for YSTAFDB",
        author="Emil Riis Hansen",
        provider="Yale University",
        dataset="YSTAFDB"
    )
    g.bind("gn", "http://sws.geonames.org/")
    g.bind("brdflo", "{}#".format(ystafdb_location_uri))
    g.bind("schema", "http://schema.org/")

    for i, label in enumerate(locations['reference_space'], 1):

        node = URIRef("{}#L_{}".format(ystafdb_location_uri, i))

        g.add((node, RDF.type, URIRef("http://schema.org/Place")))
        g.add((node, RDFS.label, Literal(label)))
        g.add((URIRef(ystafdb_location_uri), NS.prov.hadMember, node))

    write_graph(output_base_dir / "location" / "ystafdb", g)

    # Times
    file_path = os.path.join(data_dir, "reference_timeframes.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    times = pandas.read_csv(
        file_handler,
        header=0,
    )

    ystafdb_times_uri = "http://rdf.bonsai.uno/time/ystafdb"
    g = add_common_elements(
        graph=Graph(),
        base_uri=ystafdb_times_uri,
        title="Custom time for YSTAFDB",
        description="Times groupings used by YSTAFDB",
        author="Emil Riis Hansen",
        provider="Yale University",
        dataset="YSTAFDB"
    )

    BRDFTIME = Namespace("http://rdf.bonsai.uno/time/ystafdb#")
    OT = Namespace("https://www.w3.org/TR/owl-time/")
    g.bind("ot", "https://www.w3.org/TR/owl-time/")
    g.bind("brdftime", BRDFTIME)
    g.bind("schema", "http://schema.org/")

    g.add((URIRef(BRDFTIME.oneyearlong), RDF.type, OT.DurationDescription))
    g.add((URIRef(BRDFTIME.oneyearlong), OT.years, Literal(1, datatype=XSD.integer)))

    for i, label in zip(times['reference_timeframe_id'], times['reference_timeframe']):
        # TODO: Some labels are timeperiods longer than one year
        # Add node for start time of year
        if '-' in label:
            labels = label.strip().split('-')
        else:
            labels = [label, label]
        nodeStart = URIRef("{}T_{}_start".format(BRDFTIME, i))
        g.add((nodeStart, RDF.type, OT.Instant))
        g.add((nodeStart, OT.inXSDDate, Literal("{}-01-01".format(labels[0]), datatype=XSD.date)))

        # Add node for end time of year
        nodeEnd = URIRef("{}T_{}_end".format(BRDFTIME, i))
        g.add((nodeEnd, RDF.type, OT.Instant))
        g.add((nodeEnd, OT.inXSDDate, Literal("{}-12-31".format(labels[1]))))

        # Add real time node
        node = URIRef("{}T_{}".format(BRDFTIME, i))
        g.add((node, RDF.type, OT.ProperInterval))
        g.add((node, RDFS.label, Literal(label, datatype=XSD.string)))
        g.add((node, OT.hasBeginning, nodeStart))
        g.add((node, OT.hasEnd, nodeEnd))
        #g.add((node, OT.inXSDDate, Literal("{}-01-01".format(label), datatype=XSD.date)))

        # Add Provenance
        g.add((URIRef(ystafdb_times_uri), NS.prov.hadMember, nodeStart))
        g.add((URIRef(ystafdb_times_uri), NS.prov.hadMember, nodeEnd))
        g.add((URIRef(ystafdb_times_uri), NS.prov.hadMember, node))

    write_graph(output_base_dir / "time" / "ystafdb", g)


    # Unit Data
    file_path = os.path.join(data_dir, "units.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    units = pandas.read_csv(
        file_handler,
        header=0,
    )

    ystafdb_units_uri = "http://rdf.bonsai.uno/unit/ystafdb"
    g = add_common_elements(
        graph=Graph(),
        base_uri=ystafdb_units_uri,
        title="Custom units for YSTAFDB",
        description="Units used by YSTAFDB",
        author="Emil Riis Hansen",
        provider="Yale University",
        dataset="YSTAFDB"
    )

    BUNIT = Namespace("http://rdf.bonsai.uno/unit/ystafdb#")
    OM2 = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")

    g.bind("om2", OM2)
    g.bind("bunit", BUNIT)
    g.bind("schema", "http://schema.org/")

    # This is the conversion table between the ystafdb units and and the ontology-of-units-of-measure
    unitToOM2 = {
        "g": "PrefixedGram",
        "kg": "kilogram",
        "Mg": "megagram",
        "Gg": "gigagram",
        "Tg": "teragram",
        "Pg": "petagram",
        "mol": "PrefixedMole",
        "kmol": "kilomole",
        "Mmol": "megamole",
        "Gmol": "gigamole",
        "Tmol": "teramole",
        "Pmol": "petamole",
        "%": "percent",
        "Bq": "becquerel",
        "kBq": "kilobecquerel",
        "MBq": "megabecquerel",
        "GBq": "gigabecquerel",
        "TBq": "terabecquerel",
        "PBq": "petabecquerel",
        "none": {
            "mass fraction": "MassFraction",
            # TODO Check whether this is actually true...
            "mol fraction": "AmountOfSubstanceConcentration",
            "volume fraction": "VolumeFraction"
        },
        "Eg": "exagram"
    }

    for unit_id, unit, label in zip(units['unit_id'], units['unit'], units['unit_name']):
        om2Unit = unitToOM2[unit]
        if unit == "none":
            om2Unit = om2Unit[label]

        # Add node for start time of year
        node = URIRef("{}U_{}".format(BUNIT, unit_id))

        # TODO: Not sure whether all units should be OM2 PrefixedUnit types?
        g.add((node, RDF.type, OM2.PrefixedUnit))
        g.add((node, RDFS.label, Literal("{}".format(label), datatype=XSD.string)))
        g.add((node, OWL.sameAs, OM2[om2Unit]))

        # Add Provenance
        g.add((URIRef(ystafdb_units_uri), NS.prov.hadMember, node))

    write_graph(output_base_dir / "unit" / "ystafdb", g)

    # Flows
    file_path = os.path.join(data_dir, "flows.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    utf8_reader = codecs.getreader("utf-8")
    c = csv.reader(utf8_reader(file_handler))
    data_rows = []
    print("Extracting flows from YSTAFDB")
    for i, line in enumerate(c):
        if i == 0:
            header = line
            continue
        dict1 = {}
        # Multiple delimiter characters ; and , are present, along with quotes.
        # Pandas is not good in this situation, therefor this conversion
        dict1.update({key: value for key, value in zip(header, re.split(',', ",".join(line)))})
        data_rows.append(dict1)
    print("Done Extracting flows from YSTAFDB")

    # Create graph with common elements
    ystafdb_flow_uri = "http://rdf.bonsai.uno/data/ystafdb/huse"
    g = add_common_elements(
        graph=Graph(),
        base_uri=ystafdb_flow_uri,
        title="Custom locations for YSTAFDB",
        description="Country groupings used YSTAFDB",
        author="Emil Riis Hansen",
        provider="Yale University",
        dataset="YSTAFDB"
    )

    prov = Namespace("http://www.w3.org/ns/prov/ystafdb#")
    bont = Namespace("http://ontology.bonsai.uno/core#")
    data = Namespace("http://rdf.bonsai.uno/data/ystafdb/huse#")
    flow = Namespace("http://rdf.bonsai.uno/data/ystafdb/huse#")
    brdffo = Namespace("http://rdf.bonsai.uno/flowobject/ystafdb#")
    om2 = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")
    bunit = Namespace("http://rdf.bonsai.uno/unit/ystafdb#")
    btime = Namespace("http://rdf.bonsai.uno/time/ystafdb#")
    brdfat = Namespace("http://rdf.bonsai.uno/activitytype/ystafdb#")
    bloc = Namespace("http://rdf.bonsai.uno/location/ystafdb#")

    g.bind("bont", "http://ontology.bonsai.uno/core#")
    g.bind("flow", "http://rdf.bonsai.uno/data/ystafdb/huse#")
    g.bind("schema", "http://schema.org/")
    g.bind("brdffo", "http://rdf.bonsai.uno/flowobject/ystafdb#")
    g.bind("bunit", "http://rdf.bonsai.uno/unit/ystafdb#")
    g.bind("om2", "http://www.ontology-of-units-of-measure.org/resource/om-2/")
    g.bind("btime", "http://rdf.bonsai.uno/time/ystafdb#")
    g.bind("brdfat", "http://rdf.bonsai.uno/activitytype/ystafdb#")
    g.bind("bloc", "http://rdf.bonsai.uno/location/ystafdb#")

    flowCounter, activityCounter = 0, 0
    flows = pandas.DataFrame(data_rows, columns=header)
    for x in range(0, len(flows)):
        reference_timeframe_id = int(flows['reference_timeframe_id'][x])
        reference_space_id = int(flows['reference_space_id'][x])
        subsystem_id_origin = int(flows['aggregate_subsystem_module_id_origin'][x])
        subsystem_id_destination = int(flows['aggregate_subsystem_module_id_destination'][x])
        material_name_id = int(flows['material_name_id'][x])
        quantity_unit_id = int(flows['quantity_unit_id'][x])
        publication_id = flows['publication_id'][x]

        # TODO: Sometimes quantity is Null, What to do in this case?
        if flows['quantity'][x] == "NULL":
            continue
        else:
            quantity = float(flows['quantity'][x])

        # Here we create the two activities linking the flow
        activity_input = URIRef("{}#A_{}".format(ystafdb_flow_uri, activityCounter))
        g.add((activity_input, RDF.type, URIRef(bont.Activity)))
        g.add((activity_input, bont.activityType, URIRef("{}A_{}".format(brdfat, subsystem_id_origin))))
        g.add((activity_input, bont.hasTemporalExtent, URIRef("{}T_{}".format(btime, reference_timeframe_id))))
        g.add((activity_input, bont.location, URIRef("{}L_{}".format(bloc, reference_space_id))))
        activityCounter += 1

        activity_output = URIRef("{}#A_{}".format(ystafdb_flow_uri, activityCounter))
        g.add((activity_output, RDF.type, URIRef(bont.Activity)))
        g.add((activity_output, bont.activityType, URIRef("{}A_{}".format(brdfat, subsystem_id_destination))))
        g.add((activity_output, bont.hasTemporalExtent, URIRef("{}T_{}".format(btime, reference_timeframe_id))))
        g.add((activity_output, bont.location, URIRef("{}L_{}".format(bloc, reference_space_id))))
        activityCounter += 1

        # Here we create the flow
        flow = URIRef("{}#F_{}".format(ystafdb_flow_uri, flowCounter))
        g.add((flow, RDF.type, URIRef(bont.Flow)))
        g.add((flow, bont.objectType, URIRef("{}C_{}".format(brdffo, material_name_id))))
        g.add((flow, om2.hasUnit, URIRef("{}U_{}".format(bunit, quantity_unit_id))))
        g.add((flow, om2.hasNumericValue, Literal(quantity, datatype=XSD.float)))
        g.add((flow, bont.inputOf, activity_input))
        g.add((flow, bont.outputOf, activity_output))
        flowCounter += 1

        # Provenance Information
        g.add((URIRef(ystafdb_flow_uri), NS.prov.hadMember, flow))
        g.add((URIRef(ystafdb_flow_uri), NS.prov.hadMember, activity_input))
        g.add((URIRef(ystafdb_flow_uri), NS.prov.hadMember, activity_output))
        prov_uri = URIRef(bprov['dataset_{}'.format(publication_id)])
        prov_graph.add((prov_uri, prov.hadMember, flow))

        if x % 1000 == 0:
            print("Extracted {} flows and {} activities".format(x, x * 2))

    # Write graph to file
    write_graph(output_base_dir / "prov" / "ystafdb", prov_graph)
    write_graph(output_base_dir / "flow" / "ystafdb/huse", g)
