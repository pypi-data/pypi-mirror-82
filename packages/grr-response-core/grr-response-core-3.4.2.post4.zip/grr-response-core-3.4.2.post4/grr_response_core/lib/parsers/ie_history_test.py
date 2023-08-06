#!/usr/bin/env python
# Lint as: python3
"""Tests for grr.parsers.ie_history."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime
import io
import os
import struct

from absl import app
from absl.testing import absltest

from grr_response_core.lib import package
from grr_response_core.lib.parsers import ie_history
from grr_response_core.lib.rdfvalues import client as rdf_client
from grr_response_core.lib.rdfvalues import paths as rdf_paths
from grr.test_lib import test_lib


class IEHistoryParserTest(absltest.TestCase):

  def testEmpty(self):
    parser = ie_history.IEHistoryParser()

    knowledge_base = rdf_client.KnowledgeBase()
    pathspec = rdf_paths.PathSpec.OS(path="foo/bar/baz/index.dat")

    filedesc = io.BytesIO()
    filedesc.write(ie_history.IEParser.FILE_HEADER)
    filedesc.write(struct.pack("<L", 0))
    filedesc.write(struct.pack("<L", 0))

    results = list(parser.ParseFile(knowledge_base, pathspec, filedesc))
    self.assertEmpty(results)

  def testNotEmpty(self):
    parser = ie_history.IEHistoryParser()

    index_dat = os.path.join("grr_response_test", "test_data", "index.dat")
    index_dat_path = package.ResourcePath("grr-response-test", index_dat)

    knowledge_base = rdf_client.KnowledgeBase()
    pathspec = rdf_paths.PathSpec.OS(path=index_dat_path)

    with io.open(index_dat_path, mode="rb") as filedesc:
      results = list(parser.ParseFile(knowledge_base, pathspec, filedesc))

    self.assertNotEmpty(results)


class IEHistoryTest(test_lib.GRRBaseTest):
  """Test parsing of chrome history files."""

  def testBasicParsing(self):
    """Test we can parse a standard file."""
    hist_file = os.path.join(self.base_path, "index.dat")
    c = ie_history.IEParser(open(hist_file, "rb"))
    entries = [x for x in c.Parse()]

    # Check that our results are properly time ordered
    time_results = [x["mtime"] for x in entries]
    self.assertEqual(time_results, sorted(time_results))

    self.assertEqual(
        entries[1]["url"],
        "Visited: testing@http://www.google.com/chrome/chrome"
        "/eula.html")
    dt1 = datetime.datetime.utcfromtimestamp(entries[1]["ctime"] / 1e6)
    self.assertEqual(str(dt1), "2009-12-11 17:55:46.968000")
    dt2 = datetime.datetime.utcfromtimestamp(entries[-1]["ctime"] / 1e6)
    self.assertEqual(str(dt2), "2011-06-23 18:57:24.250000")
    self.assertEqual(
        entries[-1]["url"],
        "Visited: testing@mshelp://windows/?id=d063548a-3fc9-"
        "4723-99f3-b12a0c4354a8")
    self.assertLen(entries, 18)

  def testErrors(self):
    """Test empty files don't raise errors."""
    c = ie_history.IEParser(io.BytesIO())
    entries = [x for x in c.Parse()]
    self.assertEmpty(entries)


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  app.run(main)
