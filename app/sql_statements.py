"""SQL statements for the GPU database."""
from .db_utils import SQL_SelectTempl


CREATE_TABLE_STATEMENTS = [
    r'''
    CREATE TABLE "Architecture" (
    "arch_id" INTEGER,
    "arch_name" TEXT,
    PRIMARY KEY ("arch_id")
    );
    ''', r'''
    CREATE TABLE "Processor" (
    "proc_id" INTEGER,
    "proc_name" TEXT,
    "arch_id" INTEGER,
    PRIMARY KEY ("proc_id"),
    CONSTRAINT "FK_Processor.arch_id"
        FOREIGN KEY ("arch_id")
        REFERENCES "Architecture"("arch_id")
    );
    ''', r'''
    CREATE TABLE "Manufacturer" (
    "manufacturer_id" INTEGER,
    "manufacturer_name" TEXT,
    "founded_year" INTEGER,
    PRIMARY KEY ("manufacturer_id")
    );
    ''', r'''
    CREATE TABLE "Series" (
    "series_id" INTEGER,
    "series_name" TEXT,
    "release_year" INTEGER,
    PRIMARY KEY ("series_id")
    );
    ''', r'''
    CREATE TABLE "GPU" (
    "id" INTEGER,
    "name" TEXT,
    "proc_id" INTEGER,
    "clock_speed_mhz" INTEGER,
    "series_id" INTEGER,
    "manufacturer_id" INTEGER,
    "vram_size_gb" INTEGER,
    "price_cents" INTEGER,
    PRIMARY KEY ("id"),
    CONSTRAINT "FK_GPU.manufacturer_id"
        FOREIGN KEY ("manufacturer_id")
        REFERENCES "Manufacturer"("manufacturer_id"),
    CONSTRAINT "FK_GPU.proc_id"
        FOREIGN KEY ("proc_id")
        REFERENCES "Processor"("proc_id"),
    CONSTRAINT "FK_GPU.series_id"
        FOREIGN KEY ("series_id")
        REFERENCES "Series"("series_id")
    );
    '''
]
INSERT_SERIES_STATEMENT = r'''INSERT INTO Series (series_name, release_year) VALUES (?, ?);'''
INSERT_ARCH_STATEMENT = r'''INSERT INTO Architecture (arch_name) VALUES (?);'''
INSERT_MANU_STATEMENT = r'''INSERT INTO Manufacturer (manufacturer_name, founded_year) VALUES (?, ?);'''
INSERT_PROC_STATEMENT = r'''INSERT INTO Processor (proc_name, arch_id) VALUES (?, ?);'''
INSERT_GPU_STATEMENT = r'''
INSERT INTO GPU
(name, proc_id, clock_speed_mhz, series_id, manufacturer_id, vram_size_gb, price_cents)
VALUES
(?, ?, ?, ?, ?, ?, ?);
'''

SELECT_GET_GPU_DETAILS_TEMPL = SQL_SelectTempl(rf'''
SELECT
GPU.name,
Processor.proc_name,
Architecture.arch_name,
GPU.clock_speed_mhz,
Series.series_name,
Series.release_year,
Manufacturer.manufacturer_name,
Manufacturer.founded_year,
GPU.vram_size_gb,
GPU.price_cents
FROM GPU
INNER JOIN Processor ON GPU.proc_id = Processor.proc_id
INNER JOIN Architecture ON Processor.arch_id = Architecture.arch_id
INNER JOIN Series ON GPU.series_id = Series.series_id
INNER JOIN Manufacturer ON GPU.manufacturer_id = Manufacturer.manufacturer_id
{{{SQL_SelectTempl.SQL_MORE_PLACEHOLDER}}}
;
''')


SELECT_GPU_DETAILS_WITH_ID_TEMPL = SQL_SelectTempl(rf'''
SELECT
GPU.id,
GPU.name,

Processor.proc_id,
Processor.proc_name,

Architecture.arch_id,
Architecture.arch_name,

GPU.clock_speed_mhz,

Series.series_id,
Series.series_name,
Series.release_year,

Manufacturer.manufacturer_id,
Manufacturer.manufacturer_name,
Manufacturer.founded_year,

GPU.vram_size_gb,
GPU.price_cents
FROM GPU
INNER JOIN Processor ON GPU.proc_id = Processor.proc_id
INNER JOIN Architecture ON Processor.arch_id = Architecture.arch_id
INNER JOIN Series ON GPU.series_id = Series.series_id
INNER JOIN Manufacturer ON GPU.manufacturer_id = Manufacturer.manufacturer_id
{{{SQL_SelectTempl.SQL_MORE_PLACEHOLDER}}}
;
''')

SELECT_GET_ALL_GPU_DETAILS = SELECT_GET_GPU_DETAILS_TEMPL.statement

SELECT_MANU_INFO = SQL_SelectTempl(rf'''
SELECT manufacturer_name, founded_year
FROM Manufacturer
{{{SQL_SelectTempl.SQL_MORE_PLACEHOLDER}}}
;
''')

SELECT_ARCH_INFO = SQL_SelectTempl(rf'''
SELECT arch_name
FROM Architecture
{{{SQL_SelectTempl.SQL_MORE_PLACEHOLDER}}}
;
''')
