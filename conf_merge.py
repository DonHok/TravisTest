import xml.etree.ElementTree as ET


class Configuration:
    def __init__(self, list_bin, list_num, list_nfp):
        self.binary_options = list_bin
        self.numeric_options = list_num
        self.list_nfp = list_nfp

    def equals(self, configuration):
        if not len(configuration.binary_options) == len(self.binary_options):
            return False
        if not len(configuration.numeric_options) == len(self.numeric_options):
            return False
        for bin_opt in configuration.binary_options:
            partial_equal = False
            for this_bin_opt in self.binary_options:
                if bin_opt == this_bin_opt:
                    partial_equal = True
            if not partial_equal:
                return partial_equal
        for num_opt in configuration.numeric_options:
            partial_equal = False
            for this_num_opt in self.numeric_options:
                if num_opt == this_num_opt:
                    partial_equal = True
            if not partial_equal:
                return partial_equal
        return True

    def add_nfp(self, name, value):
        self.list_nfp.append((name, value))

    def to_string(self):
        this = ""
        this += "		<data column=\"Configuration\">\n"
        conf = ""
        for opt in self.binary_options:
            conf += opt + ","
        conf = conf[:-1]
        this += "		  " + conf + "\n"
        this += "		</data>\n"
        this += "		<data column=\"Variable Features\">\n"
        conf = ""
        for opt in self.numeric_options:
            conf += opt + ","
        conf = conf[:-1]
        this += "         " + conf + "\n"
        this += "		</data>\n"
        for nfp in self.list_nfp:
            this += "		<data column=\"" + nfp[0] + "\">\n"
            this += "         " + nfp[1] + "\n"
            this += "       </data>\n"
        return this


def parse_to_configurations(file):
    configurations = []
    tree = ET.parse(file)
    root = tree.getroot()
    for row in root:
        binary_options = []
        numeric_options = []
        nfps = []
        for data in row:
            if data.get("column") == "Configuration":
                binary_options = data.text.strip().split(",")
            elif data.get("column") == "Variable Features":
                numeric_options = data.text.strip().split(",")
            else:
                nfps.append((data.get("column"), data.text.strip()))
        configurations.append(Configuration(binary_options, numeric_options, nfps))
    return configurations


def main():
    first = parse_to_configurations("E:\HSMGP\PDA_numCoresAll_all_Measurements_VarFeature_AvgIt.xml")
    second = parse_to_configurations("E:\HSMGP\PDA_numCoresAll_all_Measurements_VarFeature_NumCycle.xml")
    for conf in second:
        for conf_1 in first:
            if conf_1.equals(conf):
                conf_1.add_nfp(conf.list_nfp[0][0], conf.list_nfp[0][1])
    third = parse_to_configurations("E:\HSMGP\PDA_numCoresAll_all_Measurements_VarFeature_TimeToSolution.xml")
    for conf in third:
        for conf_1 in first:
            if conf_1.equals(conf):
                conf_1.add_nfp(conf.list_nfp[0][0], conf.list_nfp[0][1])
    f = open("E:\HSMGP\PDA_numCoresAll_all_Measurements.xml", 'a')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n")
    f.write("<results>\n")
    for conf in first:
        f.write("  <row>\n")
        f.write(conf.to_string())
        f.write("  </row>\n")
    f.write("</results>")



main()