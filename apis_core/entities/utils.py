import functools
from pathlib import Path


@functools.lru_cache
def get_feature_codes():
    try:
        featurecode_list = [(None, "---")]
        self = Path(__file__)
        featurecodefile = self.parent / "featureCodes_en.txt"
        featurecodes = featurecodefile.read_text()
        featurecodes = [
            line.split("\t")
            for line in featurecodes.split("\n")
            if len(line.split("\t")) == 3
        ]
        featurecode_list.extend([(el[0], el[0] + ": " + el[1]) for el in featurecodes])
    except Exception:
        featurecode_list = [(None, "None: could not read list of feature codes")]
    return featurecode_list
