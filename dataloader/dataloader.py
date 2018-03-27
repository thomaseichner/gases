#!/usr/bin/env python

"""dataloader.py: module to load the data from the web and store it locally in a database"""

__author__ = "thomas"
__creation_date__ = '06.03.18'


import datetime
import pandas as pd
import urllib
import urllib.request
import io
import sqlalchemy

import python_general.library.configreader


class DataLoader(python_general.library.configreader.ConfigReader):
    def __init__(self, pollutant_type, time_interval=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pollutant_type = pollutant_type
        self.time_interval = time_interval
        self.timegrouping = "1SMW"
        self.config = self.config.get(self.__class__.__name__.lower())
        self.log.info("Getting data: {}, timegrouping: {}, for dates:{}".format(self.pollutant_type, self.timegrouping, self.time_interval))

    def get_raw_data(self):
        start = int(self.time_interval[0].timestamp())
        end = int(self.time_interval[1].timestamp())
        self.log.debug("Using timestamps: start: {}, end: {}".format(start, end))
        urlstring = self.config['base_url'].format(pollutant_type=self.pollutant_type, timegrouping=self.timegrouping, start_timestamp=start,
                                     end_timestamp=end)
        self.log.debug("Requesting: {}".format(urlstring))
        conn = urllib.request.urlopen(urlstring)
        answer = conn.read()
        conn.close()
        return answer

    def get_data_as_dataframe(self, data):
        frame = pd.read_csv(io.StringIO(data.decode('cp1252')), sep=';')
        frame["Zeit"] = pd.to_datetime(frame.Zeit, dayfirst=True)
        return frame

    def write_frame_to_db(self, frame, db_con, if_exists="fail"):
        frame.to_sql("{}_data".format(self.pollutant_type), con=db_con, chunksize=1000, if_exists=if_exists,
                     schema=self.config["target_db_schema"])
        self.log.info("Written data of shape: {} to db".format(frame.shape))

    def create_db_connection(self):
        connect_string = "{user}:{pwd}@{ip}/{schema}".format(user=self.config['target_db_user'],
                                                             pwd=self.config["target_db_pwd"],
                                                             ip=self.config["target_db_ip"],
                                                             schema=self.config["target_db_schema"])
        eng = sqlalchemy.create_engine('mysql+pymysql://{}'.format(connect_string), echo=True)
        self.log.info("Created target db connection for db: {}".format(connect_string))
        return eng


if __name__ == '__main__':
    dl = DataLoader('NO2', (datetime.datetime(2017, 8, 1), datetime.datetime(2017, 8, 2)), loglevel='DEBUG', config_file="../config.yml")
    frame = dl.get_data_as_dataframe(dl.get_raw_data())
    dl.write_frame_to_db(frame, dl.create_db_connection(), if_exists="append")



