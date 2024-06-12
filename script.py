PREFIX = "ex:"

def create_triple(s, p, o):
    return f"{s} {p} {o} ."

def _ex(string):
    return f"{PREFIX}{string}"

def create_literal_triple(s, p, o):
    return f"{s} {p} \"{o}\"^^xsd:string ."

def load_json(file):
    import json
    with open(file) as f:
        return json.load(f)
    
def _v(obj):
    return f"voxel_{_id(obj)}"

def _b(obj):
    return f"bbox_{_id(obj)}"

def _id(obj):
    return str(obj.get('id'))

def create_main_triple(obj):
    # create fstring from obj, use id as subject, a as predicate and "ex:Voxel" object
    return create_triple(_ex(_v(obj)), "a", _ex("Voxel"))
    
def create_id_triple(obj):
    return create_literal_triple(_ex(_v(obj)), _ex("id"), _id(obj))

def create_contains_triple(obj):
    ttl = ""
    ttl += create_triple(_ex(_v(obj)), _ex("containsElement"), _ex(obj["containsElement"])) + "\n"
    ttl += create_triple(_ex(obj["containsElement"]), "a", "bot:Element") + "\n"
    return ttl

def create_bbox_triple(obj):
    # add bbox a bbox class
    return create_triple(_ex(_v(obj)), _ex("hasBoundingBox"), _ex(_b(obj)))

def create_bbox_class_triple(obj):
    return create_triple(_ex(_b(obj)), "a", _ex("BoundingBox"))

def create_bbox_props_triple(obj):
    ttl = ""
    for k, v in obj["bbox"].items():
        ttl += create_literal_triple(_ex(_b(obj)), _ex(k), v) + "\n"
    return ttl

def create_pos_triples(obj):
    for k, v in obj.items():
        if k.endswith("Pos") or k.endswith("Neg"):
            if v == 0:
                continue
            # capitalize k (first letter)
            k = k[0].upper() + k[1:]
            predicate = _ex("hasNeighbor" + k)
            yield create_triple(_ex(_v(obj)), predicate, _ex("voxel_" + str(v)))

def add_damages(ttl):
    dmg1 = """ex:voxel_7 dot:hasDamageArea ins:DamageArea_NY0M9P1L .
ex:voxel_8 dot:hasDamageArea ins:DamageArea_NY0M9P1L .
ex:voxel_9 dot:hasDamageArea ins:DamageArea_NY0M9P1L .
ins:DamageArea_NY0M9P1L a dot:DamageArea ;
rdfs:label "DamageArea_NY0M9P1L" ;
rdfs:comment "DamageLength: None DamageWidth: None" ;
asb:Schaden_Foto "SCHADEN 3.JPG" ;
asb:Schaden_ID-Nummer-Schaden "3"^^xsd:string ;
brcomp:height "0.35"^^xsd:float ;
brcomp:length "56.75"^^xsd:float ;
brcomp:width "2.0"^^xsd:float .
    """
    dmg2 = """ex:voxel_3 dot:hasDamageArea ins:DamageArea_NY0LZ32M .
ex:voxel_4 dot:hasDamageArea ins:DamageArea_NY0LZ32M .
ex:voxel_5 dot:hasDamageArea ins:DamageArea_NY0LZ32M .
ex:voxel_6 dot:hasDamageArea ins:DamageArea_NY0LZ32M .
ins:DamageArea_NY0LZ32M a dot:DamageArea ;
rdfs:label "DamageArea_NY0LZ32M" ;
rdfs:comment "DamageLength: None DamageWidth: None" ;
asb:Schaden_ID-Nummer-Schaden "21"^^xsd:string ;
asb:Schaden_Foto "\\WIDERLAGER VORN - STIRNWAND LINKS UNTEN.JPG" ;
brcomp:height "1.72"^^xsd:float ;
brcomp:length "1.5"^^xsd:float ;
brcomp:width "4.0"^^xsd:float ;
reloc:containedInBottom ins:Abutment_Span_0 ;
reloc:containedInLeft ins:Abutment_Span_0 .
    """
    dmg3 = """ex:voxel_1 dot:hasDamageArea ins:DamageArea_RE0UU0J5 .
ex:voxel_2 dot:hasDamageArea ins:DamageArea_RE0UU0J5 .
ins:DamageArea_RE0UU0J5 a dot:DamageArea ;
rdfs:label "DamageArea_RE0UU0J5" ;
asb:Schaden_Foto "\\SCHADEN 12.JPG" ;
asb:Schaden_ID-Nummer-Schaden "12"^^xsd:string ;
reloc:containedInLeft ins:Joint_front .
    """
    return ttl + dmg1 + dmg2 + dmg3

def add_triple(turtleString, triple):
    return turtleString + triple + "\n"

def add_prefix(turtleString):
    turtleString += f"@prefix {PREFIX} <http://example.org/> .\n"
    turtleString += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ." + "\n"
    turtleString += "@prefix bot: <https://w3id.org/bot-0.3.2> ." + "\n"
    turtleString += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ." + "\n"
    turtleString += "@prefix asb: <http://www.semanticweb.org/asb/ontologies/2021/0/asb#> ." + "\n"
    turtleString += "@prefix brcomp: <http://www.semanticweb.org/brcomp/ontologies/2021/0/brcomp#> ." + "\n"
    turtleString += "@prefix reloc: <http://www.semanticweb.org/reloc/ontologies/2021/0/reloc#> ." + "\n"
    turtleString += "@prefix ins: <http://www.semanticweb.org/ins/ontologies/2021/0/ins#> ." + "\n"
    turtleString += "@prefix dot: <http://www.semanticweb.org/dot/ontologies/2021/0/dot#> ." + "\n"
    turtleString += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ." + "\n" + "\n"
    return turtleString


def write_ttl_file(turtleString, file):
    with open(file, 'w') as f:
        f.write(turtleString)

if __name__ == "__main__":
    json_data = load_json("voxelData.json")['cubes']
    turtle = ""
    turtle = add_prefix(turtle)
    for d in json_data:
        # print typeof d
        turtle = add_triple(turtle, create_main_triple(d))
        turtle += create_contains_triple(d)
        for t in create_pos_triples(d):
            turtle = add_triple(turtle, t)
        # turtle = add_triple(turtle, create_bbox_triple(d))
        # turtle = add_triple(turtle, create_bbox_class_triple(d))
        # turtle += create_bbox_props_triple(d)
    turtle = add_damages(turtle)
    write_ttl_file(turtle, "data.ttl")
    
# 7 8 9 - schaden 3
# 3 4 5 6 - schaden widerlager
# 1 and 2 - schaden12