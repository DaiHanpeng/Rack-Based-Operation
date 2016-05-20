import ConfigParser

from SampleInlabbingPosition import SampleInlabbingPosition
from SampleFlagInfo import SampleFlagInfo

CONVERSION_PARAMETER_INI_FILE = "Parameters.CFG"
SECTION_NAME = "Position2Flag"
POSITION_2_FLAG = "SamplePosition2Flag"


class SamplePositionFlagInfo(object):
    def __init__(self,r,p,f):
        self.rack = r
        self.position = p
        self.flag = f

    def __str__(self):
        return "rack: " + self.rack + " position: " + self.position + " flag: " + self.flag


class SamplePosition2FlagStratege(object):
    def __init__(self):
        self.SamplePositionFlagInfoList = []
        self.load_configuration_from_file()

    def load_configuration_from_file(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(CONVERSION_PARAMETER_INI_FILE)
        if config_parser.has_section(SECTION_NAME):
            infoList = config_parser.get(SECTION_NAME,POSITION_2_FLAG)
            sample_position_flag_info = infoList.split(";")
            for item in sample_position_flag_info:
                info = item.split(",")
                if len(info) == 3:
                    self.SamplePositionFlagInfoList.append(SamplePositionFlagInfo(info[0],info[1],info[2]))

    def position2flag(self, sample_position_info):
        if isinstance(sample_position_info, SampleInlabbingPosition):
            for info in self.SamplePositionFlagInfoList:
                if isinstance(info, SamplePositionFlagInfo):
                    if sample_position_info.rack_id == info.rack:
                        rack_position = int(sample_position_info.rack_position)
                        if (0 < rack_position <= 12) and (info.position.upper() == 'A') or\
                            (13<= rack_position <= 24) and (info.position.upper() == 'B') or\
                            (25<= rack_position <= 36) and (info.position.upper() == 'C') or\
                            (37<= rack_position <= 48) and (info.position.upper() == 'D'):
                            return SampleFlagInfo(sample_id=sample_position_info.sample_id, flag=info.flag, time_stamp=sample_position_info.time_stamp)

if __name__ == "__main__":
    convertor = SamplePosition2FlagStratege()
    position1 = SampleInlabbingPosition('123456', 1, '23729', 12, 11, '20151221115948')
    position2 = SampleInlabbingPosition('33445566', 2, '23729', 12, 34,'20160128135311')
    flag = convertor.position2flag(position1)
    if flag:
        print flag
    flag = convertor.position2flag(position2)
    if flag:
        print flag
