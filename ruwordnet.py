import lxml
from lxml import etree
from tqdm import tqdm_notebook
from typing import List, Tuple, Dict, Union


class RuWordNetInfo:
    """
    Class for extracting information from the RuWordNet thesaurus
    """

    def __init__(self):

        senses_file_n = 'data/senses.N.xml'
        senses_file_v = 'data/senses.V.xml'
        senses_file_a = 'data/senses.A.xml'

        synsets_n = 'data/synsets.N.xml'
        synsets_v = 'data/synsets.V.xml'
        synsets_a = 'data/synsets.A.xml'

        relations_file_names = ['data/synset_relations.N.xml', 'data/synset_relations.A.xml',
                                'data/synset_relations.V.xml']

        # Loading xml files
        self.senses_N = self.load_xml(senses_file_n)
        self.senses_V = self.load_xml(senses_file_v)
        self.senses_A = self.load_xml(senses_file_a)

        self.synsets_N = self.load_xml(synsets_n)
        self.synsets_V = self.load_xml(synsets_v)
        self.synsets_A = self.load_xml(synsets_a)

        # Creating dictionary mappings from words to synsets and from synsets to words
        self.word_synset_N, self.synset_word_N = self.create_word_synset_map(self.senses_N)
        self.word_synset_V, self.synset_word_V = self.create_word_synset_map(self.senses_V)
        self.word_synset_A, self.synset_word_A = self.create_word_synset_map(self.senses_A)

        # Creating dictionaries with synsets definitions
        self.defin_N = self.extract_synset_definitions(self.synsets_N)
        self.defin_V = self.extract_synset_definitions(self.synsets_V)
        self.defin_A = self.extract_synset_definitions(self.synsets_A)

        # Dictionary with the closest synset relations
        self.basic_relations = self.get_basic_relations(relations_file_names)

    @staticmethod
    def load_xml(file: str) -> lxml.etree._Element:
        """
        Load xml-file
        :param file: file name
        :return: processed xml-file
        """
        doc = etree.parse(file)
        root = doc.getroot()
        return root

    @staticmethod
    def create_word_synset_map(senses: lxml.etree._Element) -> Tuple[Dict, Dict]:

        """
        Create dictionaries with the following maps: from words to synsets and from synsets to words
        :param senses: loaded xml-file with senses
        :return: two dictionaries: {words: synsets} and {synset: words}
        """

        synset_dict = {}
        synonyms = {}

        for child in senses:
            name = child.attrib['name'].lower()

            if name not in synset_dict.keys():
                synset_dict[name] = []
            synset_dict[name].append(child.attrib['synset_id'])

            if child.attrib['synset_id'] not in synonyms.keys():
                synonyms[child.attrib['synset_id']] = []

            synonyms[child.attrib['synset_id']].append(name)

        return synset_dict, synonyms

    @staticmethod
    def extract_synset_definitions(synsets: lxml.etree._Element) -> Dict:
        """
        Extract synset definitipns from xml-file
        :param synsets: synsets xml-file
        :return: dictionary with ruthes names and definitions
        """

        definitions = {}
        for child in synsets:
            definitions[child.attrib['id']] = {'ruthes_name': child.attrib['ruthes_name'],
                                               'definition': child.attrib['definition']}
        return definitions

    def get_basic_relations(self, relations_files: List[str]) -> Dict:

        """
        Create dictionary with synsets as keys and all the close relations as values
        :param relations_files: list of synset relations file names
        :return: dictionary of the following format: {'N12658': {'hypernym': ['N37195', 'N14084'],
        'part holonym': ['N35721'], 'POS-synonymy': ['V46672']}, ...}
        """

        relatives_dict_new = {}

        for file in relations_files:
            root = self.load_xml(file)
            par_id_prev = ''  # previous parent_id
            for child in root:

                if par_id_prev == child.attrib['parent_id']:
                    if child.attrib['name'] in relatives_dict_new[child.attrib['parent_id']].keys():
                        relatives_dict_new[child.attrib['parent_id']][child.attrib['name']].append(
                            child.attrib['child_id'])
                    else:
                        relatives_dict_new[child.attrib['parent_id']][child.attrib['name']] = [child.attrib['child_id']]
                        par_id_prev = child.attrib['parent_id']

                else:
                    relatives_dict_new[child.attrib['parent_id']] = {}

                    relatives_dict_new[child.attrib['parent_id']][child.attrib['name']] = [child.attrib['child_id']]
                    par_id_prev = child.attrib['parent_id']

        return relatives_dict_new

    def extract_word_synset_number(self, word: str, full_info: bool = False) -> List:

        """
        Extract synsets for the given word
        :param word: query word
        :param full_info: True if we want to print ruthes name and definition of the output synset
        :return: list of synsets (optionally with additional info)
        """

        if word in self.word_synset_N.keys():
            synsets = self.word_synset_N[word]

        elif word in self.word_synset_V.keys():
            synsets = self.word_synset_V[word]

        elif word in self.word_synset_A.keys():
            synsets = self.word_synset_A[word]
        else:
            return ['No such word in RuWordNet']

        if full_info:
            output_info = []

            for syn in synsets:
                synset_info = self.show_synset_definitions(syn)
                output_info.append([syn, synset_info])
            return output_info
        else:
            return synsets

    def show_synset_definitions(self, synset_number: str) -> Dict:

        """
        Return synset definition
        :param synset_number: synset under consideration
        :return: dictionary like this {'ruthes_name': 'КОДИРОВАНИЕ ОТ ЗАВИСИМОСТИ', 'definition': ''}
        """

        if synset_number in self.defin_N.keys():
            return self.defin_N[synset_number]

        elif synset_number in self.defin_N.keys():
            return self.defin_N[synset_number]

        elif synset_number in self.defin_N.keys():
            return self.defin_N[synset_number]

        else:
            return {}

    def show_synset_words(self, synset_number: str) -> List[str]:

        """
        Print all the words from a given synset (synonyms)
        :param synset_number: synset id
        :return: list of words
        """

        if synset_number in self.synset_word_N.keys():
            return self.synset_word_N[synset_number]

        elif synset_number in self.synset_word_V.keys():
            return self.synset_word_V[synset_number]

        elif synset_number in self.synset_word_A.keys():
            return self.synset_word_A[synset_number]

        else:
            return ['No such synset in the thesaurus']

    def show_synonyms(self, word: str) -> Union[List[Dict], str]:

        """
        Extract synonyms for a given word
        :param word: word for which we want to find synonyms
        :return: list of synonyms with synset info: [{'synset_id': 'N29948', 'synonyms': ['ножка'],
        'ruthes_name': 'НОГА (НИЖНЯЯ КОНЕЧНОСТЬ)'}]
        """

        if word in self.word_synset_N.keys():
            synsets = self.word_synset_N[word]

        elif word in self.word_synset_V.keys():
            synsets = self.word_synset_V[word]

        elif word in self.word_synset_A.keys():
            synsets = self.word_synset_A[word]

        else:
            return 'No such word in RuWordNet'

        output_info = []

        for syn in synsets:
            synonyms = self.show_synset_words(syn)
            if word in synonyms:
                synonyms.remove(word)

            defin = self.show_synset_definitions(syn)['ruthes_name']
            output_info.append({'synset_id': syn, 'synonyms': synonyms, 'ruthes_name': defin})

        return output_info

    def show_basic_synset_relations(self, synset_number: str) -> Dict:
        """
        Show synsets that are connected to the synset under consideration
        :param synset_number: synset id
        :return: dictionary with relations that connect this synset to others (the most close ones)
        """

        if synset_number in self.basic_relations:
            return self.basic_relations[synset_number]
        else:
            return {}

    def show_synset_relations_with_words(self, synset_number: str, print_synsets: bool = False,
                                         relations: Union[List[str], str] = 'all') -> Dict:
        """
        Show the words that are connected to a synset with particular relations (only the closest relations)
        :param synset_number: synset id
        :param print_synsets: show which words belong to which synsets
        :param relations: what relations should we output (either 'all' if all the possible relations or
        list with other relations of interest). If some relation is present in a list but there
        is no such relation for the given synset, this relation won't be in the output.
        :return: dictionary with words and relations.
        E.g., params: 'N12658', relations=['hypernym', 'domain'], print_synsets=True
        output:
        {'hypernym': {'N37195': ['медицинская помощь','врачебная помощь','медицинское обслуживание',...],
        'N14084': ['гипнотизация', 'гипнотизирование', 'гипноз',...]},
        'domain': {'N30873': ['медицина', 'медицинская сфера']}}
        """

        relatives_dict = self.show_basic_synset_relations(synset_number)
        if relatives_dict != {}:

            relatives_dict_words = dict()
            for relation, synsets in relatives_dict.items():

                for syn in synsets:

                    if print_synsets:

                        if relation not in relatives_dict_words:
                            relatives_dict_words[relation] = {}
                        if syn not in relatives_dict_words[relation]:
                            relatives_dict_words[relation][syn] = []

                        relatives_dict_words[relation][syn].extend(self.show_synset_words(syn))

                    else:
                        if relation not in relatives_dict_words:
                            relatives_dict_words[relation] = []

                        relatives_dict_words[relation].extend(self.show_synset_words(syn))
        else:
            return {}

        if relations == 'all':
            return relatives_dict_words
        else:
            final_dict = {relation: relatives_dict_words[relation] for relation in relations if
                          relation in relatives_dict_words}
            return final_dict

    def show_word_closest_relatives(self, word: str, synset: str = '', relations: Union[List[str], str] = 'all',
                                    print_synsets: bool = False):
        """
        Extract the most closely related words for the given word
        :param word: word for which we want to output the closest relatives
        :param synset: synset id (optional, if only we want to specify for which word
         sense we want to extract relatives)
        :param relations: what relations should we output (either 'all' if all the possible relations or
        list with other relations of interest). If some relation is present in a list but there
        is no such relation for the given synset, this relation won't be in the output.
        :param print_synsets: show which words belong to which synsets
        :return: dictionary with words and relations.
        E.g., params: 'лук', relations=['hypernym'], print_synsets=True
        {'N12915': {'hypernym': {'N27462': ['оружие']}},
         'N30469': {'hypernym': {'N41975': ['лучок', 'лук']}},
         'N41975': {'hypernym': {'N39040': ['овощ',
            'овощи',
            'овощная продукция',
            'продукция овощных культур'],
           'N31727': ['овоще-бахчевая культура',
            'овощная культура',
            'плодоовощная культура',
            'огородное растение',
            'овощебахчевая культура'],
           'N41010': ['луковичное растение']}}}
        """

        if synset != '':
            # Simple check-up
            synsets = self.extract_word_synset_number(word)
            if synset not in synsets:
                print('Inconsistence between the given word and the synset! The output will be given for the'
                      ' synset specified in parameters')
            relatives = self.show_synset_relations_with_words(synset, relations=relations, print_synsets=print_synsets)
        else:
            relatives = {}
            synsets = self.extract_word_synset_number(word)
            if synsets != ['No such word in RuWordNet']:
                for syn in synsets:
                    relatives[syn] = self.show_synset_relations_with_words(syn, relations=relations,
                                                                           print_synsets=print_synsets)
            else:
                relatives = {}
        return relatives

    def extract_polysesmous_words(self, pos: str = 'Noun', output: str = 'lemmas') -> List:
        """
        Extract list of polysemous words for a given part of speech
        :param pos: part of speech tag, possible tags: Noun, Verb, Adj
        :param output: type of the output - lemmas or unlemmatized words
        :return: list of polysemous words
        """

        poly_words = []

        if pos == 'Noun':
            senses = self.senses_N
        elif pos == 'Verb':
            senses = self.senses_V
        elif pos == 'Adj':
            senses = self.senses_A
        else:
            print('Invalid POS-tag')
            return []

        for child in tqdm_notebook(senses):

            mean = child.attrib['meaning']

            if output == 'lemmas':
                name = child.attrib['lemma'].lower()
            else:
                name = child.attrib['name'].lower()

            if name not in poly_words and mean != '1':
                poly_words.append(name)

        return poly_words

    def extract_monosesmous_words(self, pos: str = 'Noun', output: str = 'lemmas') -> List:
        """
        Extract list of monosemous words for a given part of speech
        :param pos: part of speech tag, possible tags: Noun, Verb, Adj
        :param output: type of the output - lemmas or unlemmatized words
        :return: list of monosemous words
        """

        mono_words = []

        if pos == 'Noun':
            senses = self.senses_N
        elif pos == 'Verb':
            senses = self.senses_V
        elif pos == 'Adj':
            senses = self.senses_A
        else:
            print('Invalid POS-tag')
            return []

        for child in tqdm_notebook(senses):

            mean = child.attrib['meaning']

            if output == 'lemmas':
                name = child.attrib['lemma'].lower()
            else:
                name = child.attrib['name'].lower()

            if name not in mono_words and mean == '1':
                mono_words.append(name)

        return mono_words

