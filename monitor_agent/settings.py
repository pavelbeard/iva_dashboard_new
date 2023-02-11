import os

DEBUG = os.getenv("DEBUG", False)

CRUTCH = os.getenv("CRUTCH", True)

MONITOR_AGENT_ADDRESS = os.getenv("MONITOR_AGENT_ADDRESS", "localhost")
MONITOR_AGENT_PORT = os.getenv("MONITOR_AGENT_PORT", 8012)
POSTGRES_DB_ADDRESS = os.getenv("POSTGRES_DB_ADDRESS", "localhost")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT", 8002)
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "test_db")
POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER", "test_db")
POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD", "test_db")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", b'Thm1rA590U9IBSMMIlKWgBSPwbP30nz4keJR6N4RXjI=')

CRUTCH_DATA = """
Cluster Summary:
  * Stack: corosync
  * Current DC: ivcs-main-1 (version 2.0.5-ba59be7122) - partition with quorum
  * Last updated: Wed Dec 28 15:52:53 2022
  * Last change:  Tue Nov 15 10:50:51 2022 by root via crm_attribute on ivcs-main-1
  * 2 nodes configured
  * 14 resource instances configured

Node List:
  * Online: [ ivcs-main-1 ivcs-main-2 ]

Full List of Resources:
  * Resource Group: db-group:
    * db-ip	(ocf::heartbeat:IPaddr2):	 Started ivcs-main-1
  * Resource Group: filestorage-group:
    * filestorage-fs	(ocf::heartbeat:Filesystem):	 Started ivcs-main-1
    * filestorage-ip	(ocf::heartbeat:IPaddr2):	 Started ivcs-main-1
    * samba	(systemd:smbd):	 Started ivcs-main-1
  * Resource Group: ivcs-server-group:
    * ivcs-server-ip	(ocf::heartbeat:IPaddr2):	 Started ivcs-main-1
    * ivcs-server	(systemd:ivcs-server):	 Started ivcs-main-1
  * Clone Set: drbd-ms [drbd] (promotable):
    * Masters: [ ivcs-main-1 ]
    * Slaves: [ ivcs-main-2 ]
  * Clone Set: ivcs-db-ms [ivcs-db] (promotable):
    * Masters: [ ivcs-main-1 ]
    * Slaves: [ ivcs-main-2 ]
  * Clone Set: diskspace-clone [diskspace]:
    * Started: [ ivcs-main-1 ivcs-main-2 ]
  * Clone Set: monitor-clone [monitor]:
    * Started: [ ivcs-main-1 ivcs-main-2 ]
"""