import pymysql


class ncbDB:
    # I have to retrieve basic configuration attributes, listed below, from system config file
    # on ApplSrv, for example : /etc/ncb_applsrv/ncb_applsrv.conf
    hostname = 'applsrv01'
    db_server = '65.48.98.242'  # It's HA Proxy - DB front-end server
    conferenceConfigDBname = 'nbs_conf'  # both server config and conference config are in the same DB
    conferenceConfigDBname_user = 'haproxy'
    conferenceConfigDBname_passwd = 'haproxy'
    conferenceMediaStoragePath = '/media/conference/'  # NFS mount point
    conferenceDBcurs = None
    connect_db = None

    def __init__(self):
        try:
            self.connect_db = pymysql.connect(self.db_server,
                                              self.conferenceConfigDBname_user,
                                              self.conferenceConfigDBname_passwd,
                                              self.conferenceConfigDBname,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
            # self.conferenceDBcurs = self.connect_db.cursor()
        except:
            logging.critical("Can not establish connection to configuration DB: %s", self.conferenceConfigDBname)

            # !! NOTE !! I have to insert here something indicating that the object is failed

    def ncb_getQuery(self,
                     querySQL):  # the method executes SQL query and returns all fetched rows. Otherwise it returns None
        try:
            with self.connect_db.cursor() as self.conferenceDBcurs:
                self.conferenceDBcurs.execute(querySQL)
                result = self.conferenceDBcurs.fetchall()
                if len(result) == 1:
                    return result[0]
                return (result)
        except:
            logging.critical('ERROR: Can not retrieve data from Conference DB. Call to support immediately')
            return None

    def ncb_pushQuery(self, querySQL):  # the method executes SQL query to push data into DB.
        try:
            with self.connect_db.cursor() as self.conferenceDBcurs:
                self.conferenceDBcurs.execute(querySQL)
                self.conferenceDBcurs.commit()
                return True
        except:
            logging.critical('ERROR: Can not push a data into Conference DB. Call to support immediately')
            return False

    def listdicttodict(self,
                       listdict):  # if more than one rows are retrieved - it gets first row from the list as a dictionary
        return listdict[0]

    def getGlobalMediaPath(self):
        if not os.path.exists(self.conferenceMediaStoragePath):  # check it out whether it exist
            return None  # if it doesn't - return None
        else:
            return self.conferenceMediaStoragePath  # otherwise return the path

    def __del__(self):
        self.connect_db.close()
