## begin license ##
#
# "Meresco Oai" are components to build Oai repositories, based on
# "Meresco Core" and "Meresco Components".
#
# Copyright (C) 2011 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2011 Stichting Kennisnet http://www.kennisnet.nl
# Copyright (C) 2012-2014, 2016 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2013-2014 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2014 Netherlands Institute for Sound and Vision http://instituut.beeldengeluid.nl/
# Copyright (C) 2016 Koninklijke Bibliotheek (KB) http://www.kb.nl
# Copyright (C) 2016 SURFmarket https://surf.nl
#
# This file is part of "Meresco Oai"
#
# "Meresco Oai" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# "Meresco Oai" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Meresco Oai"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##

#######################
# wilkos-dans, 20190718
# Changed #prefixIdentifier() and  #unprefixIdentifier() methods to accomodate the requiement by OpenAIRE Advance to put the CERIF type in the identifier (=added semantics, IMHO=Bad)
# Files affected:
# - oaipmh.py
# - oairecord.py
# - oairepository.py
#######################

from xml.sax.saxutils import escape as xmlEscape

from weightless.core import compose
from meresco.core import Transparent
from meresco.core.generatorutils import decorate

#########
from re import findall
#########

CERIF_GENRE_MAPPING = {'person':'Persons/', 'research':'Projects/', 'organisation':'OrgUnits/', 'dataset':'Products/', 'software':'Products/', 'publication':'Publications/', 'patent':'Patents/', 'funding':'Fundings/'}

class OaiRecord(Transparent):
    def __init__(self, repository=None, preciseDatestamp=False, **kwargs):
        Transparent.__init__(self, **kwargs)
        self._repository = repository
        self._preciseDatestamp = preciseDatestamp

    def oaiRecordHeader(self, record, **kwargs):
        isDeletedStr = ' status="deleted"' if record.isDeleted else ''
        datestamp = record.getDatestamp(preciseDatestamp=self._preciseDatestamp)
        identifier = record.identifier.encode('utf-8')

#########
        str_genre = '' # Get 'genre' from normalized short format: We cannot tell from the identifier.
        try:
            data = yield self.any.retrieveData(identifier=record.identifier, name="knaw_short")
            genre = findall("<genre>(.+?)</genre>", data)
            if len(genre) >= 1: str_genre = genre[0]
            if not str_genre in CERIF_GENRE_MAPPING.keys(): str_genre = "publication"
            # if str_genre == 'research': # Might be a Funding... <type_nl>Financieringsprogramma</type_nl>
            #     metadata = yield self.any.retrieveData(identifier=record.identifier, name="metadata")
            #     if len(findall("<type_nl>Financieringsprogramma</type_nl>", metadata)) >= 1: str_genre = "funding"
        except IOError:
            pass
        if self._repository:
            identifier = self._repository.prefixIdentifier(identifier, CERIF_GENRE_MAPPING.get(str_genre, ''))
########            
        yield '<header%s>' % isDeletedStr
        yield '<identifier>%s</identifier>' % xmlEscape(identifier)
        yield '<datestamp>%s</datestamp>' % datestamp
        yield self._getSetSpecs(record)
        yield '</header>'

    def oaiRecord(self, record, metadataPrefix, fetchedRecords=None):
        yield '<record>'
        yield self.oaiRecordHeader(record)

        if not record.isDeleted:
            yield '<metadata>'
            if not fetchedRecords is None:
                try:
                    yield fetchedRecords[record.identifier]
                except KeyError:
                    pass
            else:
                try:
                    data = yield self.any.retrieveData(identifier=record.identifier, name=metadataPrefix)
                    yield data
                except IOError:
                    pass
            yield '</metadata>'
            try:
                provenance = compose(self.all.provenance(record.identifier))
                for line in decorate('<about>', provenance, '</about>'):
                    yield line
            except KeyError:
                pass
        yield '</record>'

    def _getSetSpecs(self, record):
        if record.sets:
            return ''.join('<setSpec>%s</setSpec>' % xmlEscape(setSpec) for setSpec in record.sets)
        return ''
