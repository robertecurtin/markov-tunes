# Markov Tunes

This project aims to automatically generate a traditional irish tune. It leverages the ABC music file format and the music archives at TheSession.org to build its database, and then processes that data and uses Markov chains to generate a tune.

The project is currently in early development. It can process measures of a tune and then assemble them using Markov chains.

## Usage

Run TuneScraper.py to download tunes from TheSession.org and assemble them into a usable database.
Run LinkMaker.py to assemble Markov links for a given tune type and key (currently, this is hardcoded to D major reels)

## Future Goals

- Generalize LinkMaker.py to take in a tune type and key.
- Extract phrases by beat rather than by measure - for example, pulling out three beats at a time from a jig.
- Devise a method other than Mar:w
ov chains to intellegently assemble a tune. Perhaps this could involve notating the phrase location within a tune and then leverating that knowledge to create a tune with traditional Irish structure.
