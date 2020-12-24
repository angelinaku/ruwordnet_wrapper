# ruwordnet_wrapper
Python wrapper to work with RuWordNet thesaurus

In order to process thesaurus data, you first need to obtain xml-files of the thesaurus and put them in the data folder.  
The instruction of how to obtain files is given here: [ruwordnet.ru](https://ruwordnet.ru/en/)

To extract information from the RuWordNet graph, you need to clone this repo and run the following code:

```
from ruwordnet import RuWordNetInfo
ruw = RuWordNetInfo()
```

* Extract the synsets that a word belongs to:
```
ruw.extract_word_synset_number('нога')
```

* Extarct a synset definition:
```
ruw.show_synset_definitions('N12658')
```

* Print all the words from a given synset:
```
ruw.show_synset_words('A1')
```

* Extract all the synonyms to a given word:

```
ruw.show_synonyms('рука')
```

* Show all the synsets that are closely connected to a given synset:
```
ruw.show_basic_synset_relations('N12658')
```

* Show the words closely connected to a given synset (with relations specified):
```
ruw.show_synset_relations_with_words('N12658', relations=['hypernym', 'domain'], print_synsets=True)
ruw.show_synset_relations_with_words('N12658', relations='all')
```

* Show the words connected to a given words with specified semantic relations (only the closest relations are available):
```
ruw.show_word_closest_relatives('лук', relations=['hypernym'], print_synsets=True)
```

* Obtain a list of polysemous/monosemous words for a given part of speech:
```
ruw.extract_polysesmous_words('Noun')
ruw.extract_monosesmous_words('Verb')
```
