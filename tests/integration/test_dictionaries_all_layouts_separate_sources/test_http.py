import math
import os

import pytest

from helpers.cluster import ClickHouseCluster
from helpers.dictionary import Dictionary, DictionaryStructure, Field, Layout, Row
from helpers.external_sources import SourceHTTP

from .common import *

SOURCE = SourceHTTP("SourceHTTP", "localhost", "9000", "clickhouse_h", "9000", "", "")

cluster = None
node = None
simple_tester = None
complex_tester = None
ranged_tester = None
test_name = "http"


def setup_module(module):
    global cluster
    global node
    global simple_tester
    global complex_tester
    global ranged_tester

    simple_tester = SimpleLayoutTester(test_name)
    simple_tester.cleanup()
    simple_tester.create_dictionaries(SOURCE)

    complex_tester = ComplexLayoutTester(test_name)
    complex_tester.create_dictionaries(SOURCE)

    ranged_tester = RangedLayoutTester(test_name)
    ranged_tester.create_dictionaries(SOURCE)
    # Since that all .xml configs were created

    cluster = ClickHouseCluster(__file__)

    main_configs = []
    main_configs.append(os.path.join("configs", "disable_ssl_verification.xml"))

    dictionaries = simple_tester.list_dictionaries()

    cluster.add_instance("clickhouse_h", main_configs=main_configs)

    node = cluster.add_instance(
        "http_node", main_configs=main_configs, dictionaries=dictionaries
    )


def teardown_module(module):
    simple_tester.cleanup()


@pytest.fixture(scope="module")
def started_cluster():
    try:
        cluster.start()

        simple_tester.prepare(cluster)
        complex_tester.prepare(cluster)
        ranged_tester.prepare(cluster)

        yield cluster

    finally:
        cluster.shutdown()


@pytest.mark.parametrize("layout_name", sorted(LAYOUTS_SIMPLE))
def test_simple(started_cluster, layout_name):
    simple_tester.execute(layout_name, node)


@pytest.mark.parametrize("layout_name", sorted(LAYOUTS_COMPLEX))
def test_complex(started_cluster, layout_name):
    complex_tester.execute(layout_name, node)


@pytest.mark.parametrize("layout_name", sorted(LAYOUTS_RANGED))
def test_ranged(started_cluster, layout_name):
    ranged_tester.execute(layout_name, node)
