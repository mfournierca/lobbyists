from os.path import dirname, join

TIME_FORMAT = "%Y-%m-%d"
DATA_ROOT = join(dirname(__file__), "..", "data")

SOURCE_DATA_URL = (
    "http://29040.vws.magma.ca/od-do_dl.php?f=Communications_OCL_CAL.zip"
)
SOURCE_DATA_DICTIONARY_URL = (
    "http://29040.vws.magma.ca/od-do_dl.php?f="
    "Communications_Dictionary_Dictionnaire_Communication.xlsx"
)
SOURCE_DATA_ARCHIVE = join(DATA_ROOT, "source.zip")
SOURCE_DATA_ROOT = join(DATA_ROOT, "source")
SOURCE_DATA_DICTIONARY_FILE = join(SOURCE_DATA_ROOT, "dictionary.xlsx")

SQL_SCRIPTS_DIR = join(dirname(__file__), "db", "sql")

