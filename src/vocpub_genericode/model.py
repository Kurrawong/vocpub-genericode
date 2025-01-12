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
    identifier: str
    language: str

    def __init__(self, identifier=None, language=None):
        self.identifier = identifier
        self.language = language

    def to_etree(self):
        pass


@dataclass
class LongName(Genericode):
    value: str

    def __init__(self, value, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.value = value


@dataclass
class AlternateFormatLocationUri(Genericode):
    value: str
    mime_type: str = None

    def __init__(self, value, mime_type, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.value = value
        self.mime_type = mime_type


@dataclass
class Identifier(Genericode):
    value: str

    def __init__(self, value, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.value = value


@dataclass
class Agency(Genericode):
    short_name: str = None
    long_name: LongName = None

    def __init__(self, short_name=None, long_name=None, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.short_name = short_name
        self.long_name = long_name


@dataclass
class Identification(Genericode):
    short_name: str
    long_names: list[LongName] = None
    version: str = None
    canonical_uri: str = None
    canonical_version_uri: str = None
    location_uris: list[str] = None
    alternative_location_uris: list[AlternateFormatLocationUri] = None
    publisher: Agency = None
    maintainer: Agency = None

    def __init__(
            self,
            short_name=None,
            long_names=None,
            version=None,
            canonical_uri=None,
            canonical_version_uri=None,
            location_uris=None,
            alternative_location_uris=None,
            publisher=None,
            maintainer=None,
            identifier=None,
            language=None):
        super().__init__(identifier=identifier, language=language)
        self.short_name = short_name
        self.long_names = long_names
        self.version = version
        self.canonical_uri = canonical_uri
        self.canonical_version_uri = canonical_version_uri
        self.location_uris = location_uris
        self.alternative_location_uris = alternative_location_uris
        self.publisher = publisher
        self.maintainer = maintainer

    def to_etree(self):
        root = etree.Element("Identification")

        return root

@dataclass
class Column(Genericode):
    datatype: URIRef
    required: bool = False
    identification: Identification = None

    def __init__(self, identifier, datatype, identification=None, required=False, language=None):
        super().__init__(identifier, language=language)
        self.datatype = datatype
        self.required = required
        self.identification = identification

    def to_etree(self):
        super().to_etree()

        """
          <Column Id="code" Use="required">
             <ShortName>Code</ShortName>
             <Data Type="normalizedString" Lang="en"/>
          </Column>        
        """
        root = etree.Element("Column")

        root.attrib["Id"] = self.identifier

        dt = etree.Element("Data")
        dt.attrib["Type"] = str(self.datatype).split("#")[1]
        if self.language is not None:
            dt.attrib["Lang"] = self.language

        root.attrib["Use"] = "required" if self.required else "optional"
        if self.identification is not None:
            if self.identification.short_name is not None:
                sn = etree.Element("ShortName")
                sn.text = self.identification.short_name
                root.append(sn)

        root.append(dt)

        return root


@dataclass
class ColumnRef(Genericode):
    identification: Identification
    datatype: URIRef
    externalRef: str


@dataclass
class Key(Genericode):
    columns: list[Column | ColumnRef]  # 0..*
    identification: Identification

    def __init__(self, columns, identification=None, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.columns = columns
        self.identification = identification


@dataclass
class KeyRef(Genericode):
    id: str
    externalRef: str


@dataclass
class ColumnSet(Genericode):
    """A column set document has the root element <gc:ColumnSet>. It contain definitions of genericode columns or keys that can be imported into code list documents or into other column set documents."""
    columns: dict[str, Column]
    keys: dict[str, Key]
    identification: Identification = None

    def __init__(self, columns, keys, identification=None, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.columns = columns
        self.keys = keys
        self.identification = identification


@dataclass
class CodeListValues(Genericode):
    pass

@dataclass
class CodeList(Genericode):
    """A code list document has the root element <gc:CodeList>. It contains metadata describing the code list as a whole, as well as explicit code list data – codes and associated values."""
    identification: Identification
    defined_column_sets: list[Column]  # 1..*
    imported_column_sets: list[Column]  # 0..*
    # code_list: CodeListValues

    def __init__(self, defined_column_sets, imported_column_sets=None, identification=None, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.defined_column_sets = defined_column_sets
        self.imported_column_sets = imported_column_sets
        self.identification = identification

    def to_etree(self):
        etree.register_namespace("gc", "http://docs.oasis-open.org/codelist/ns/genericode/1.0/")
        root = etree.Element(
            etree.QName("gc", "CodeList")
        )
        # root.attrib["xmlns:gc"] = "http://docs.oasis-open.org/codelist/ns/genericode/1.0/"
        if self.identification is not None:
            # mine the Identification, rather than use it directly
            root.append(self.identification.to_etree())
        for defined_column_set in self.defined_column_sets:
            root.append(defined_column_set.to_etree())

        return root


@dataclass
class ExplicitCodeList(CodeListValues):
    pass


@dataclass
class SimpleCodeList(ExplicitCodeList):
    pass


@dataclass
class ImplicitCodeList(CodeListValues):
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
    short_name: str = None
    long_name: str = None

    def __init__(self, short_name=None, long_name=None, identifier=None, language=None):
        super().__init__(identifier=identifier, language=language)
        self.short_name = short_name
        self.long_name = long_name