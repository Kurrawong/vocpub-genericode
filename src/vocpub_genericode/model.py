from typing import Dict
from dataclasses import dataclass
# from rdflib.namespace import XSD
from rdflib import URIRef
from lxml import etree


#
#   VocPub Classes
#
class VocPub:
    pass


class ConceptScheme(VocPub):
    pass


class Concept(VocPub):
    pass


class Collection(VocPub):
    pass


class Agent(VocPub):
    pass


#
#   Genericode Classes
#
@dataclass
class Genericode:
    def to_etree(self):
        pass


@dataclass
class Column(Genericode):
    id: str
    datatype: URIRef
    short_name: str
    required: bool = False
    canonical_uri: str = None
    canonical_version_uri: str = None
    language: str = None
    long_names: list[str] = None
    extra_canonical_identification_uris: list[str] = None

    def to_etree(self):
        super().to_etree()

        """
          <Column Id="code" Use="required">
             <ShortName>Code</ShortName>
             <Data Type="normalizedString" Lang="en"/>
          </Column>        
        """
        root = etree.Element("Column")
        root.attrib["Id"] = self.id
        root.attrib["Use"] = "required" if self.required else "optional"
        sn = etree.Element("ShortName")
        sn.text = self.short_name
        root.append(sn)
        dt = etree.Element("Data")
        dt.attrib["Type"] = str(self.datatype).split("#")[1]
        if self.language:
            dt.attrib["Lang"] = self.language
        root.append(dt)
        return root


@dataclass
class ColumnRef(Genericode):
    id: str
    canonical_uri: str
    canonical_version_uri: str
    datatype: URIRef
    externalRef: str


@dataclass
class Key(Genericode):
    id: str
    short_name: str
    columns: list[Column | ColumnRef]  # 0..*
    long_names: list[str] = None
    extra_canonical_identification_uris: list[str] = None



@dataclass
class KeyRef(Genericode):
    id: str
    externalRef: str


@dataclass
class ColumnSet(Genericode):
    """A column set document has the root element <gc:ColumnSet>. It contain definitions of genericode columns or keys that can be imported into code list documents or into other column set documents."""
    id: str
    columns: dict[str, Column]
    keys: dict[str, Key]
    short_name: str
    long_names: list[str]
    version: str
    canonical_uri: str
    canonical_version_uri: str
    location_uris: list[str]
    alternative_location_uris: list[str]
    publisher: str
    maintainer: str


@dataclass
class CodeList(Genericode):
    """A code list document has the root element <gc:CodeList>. It contains metadata describing the code list as a whole, as well as explicit code list data – codes and associated values."""
    id: str
    required_columns: list[Column]  # 1..*
    optional_columns: list[Column]  # 0..*
    keys: list[Key]  # 1..*
    defined_column_sets: list[Column]  # 1..*
    imported_column_sets: list[Column]  # 0..*


@dataclass
class ExplicitCodeList(CodeList):
    pass


@dataclass
class SimpleCodeList(ExplicitCodeList):
    pass


@dataclass
class ImplicitCodeList(CodeList):
    pass


@dataclass
class CodeListMetadata(ImplicitCodeList):
    pass


@dataclass
class CodeListSet(Genericode):
    """A code list set document has the root element <gc:CodeListSet>. It contains references to particular versions of code lists, and can also contain version-independent references to code lists. A code list set document can be used to define a particular configuration of versions of code lists that are used by a project, application, standard, etc."""
    pass


@dataclass
class Agency(Genericode):
    """"Details of an agency which produces code lists or related artifacts."""
    id: str
    short_name: str
    long_names: list[str]