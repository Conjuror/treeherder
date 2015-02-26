# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from treeherder.log_parser.parsers import TinderboxPrintParser


# a list of test cases for the tinderbox printlines parser
# every test case is composed by (input, output), where
# input is a tinderbox print line and output is a job artifact
# generated by the parser
TINDERBOX_TEST_CASES = (
    (
        (
            'TinderboxPrint: <a title="libxul_link" '
            'href=\'http://graphs.mozilla.org/graph.html#tests=[[205,63,8]]\'>'
            'libxul_link:2918047744'
            '</a>'
        ),
        [{
            'content_type': 'link',
            'title': None,
            'url': 'http://graphs.mozilla.org/graph.html#tests=[[205,63,8]]',
            'value': 'libxul_link:2918047744'
        }]
    ),

    (
        (
            'TinderboxPrint: sources.xml: http://stage.mozilla.org/pub/mozilla.org/'
            'b2g/manifests/depend/mozilla-central/hamachi-eng/20140718040333/'
            'sources-5d0aad07bd13e04de0cd7befc0e2b83a.xml'
        ),
        [{
            'content_type': 'link',
            'title': 'sources.xml',
            'url': (
                'http://stage.mozilla.org/pub/mozilla.org/'
                'b2g/manifests/depend/mozilla-central/hamachi-eng/20140718040333/'
                'sources-5d0aad07bd13e04de0cd7befc0e2b83a.xml'
            ),
            'value': (
                'http://stage.mozilla.org/pub/mozilla.org/'
                'b2g/manifests/depend/mozilla-central/hamachi-eng/20140718040333/'
                'sources-5d0aad07bd13e04de0cd7befc0e2b83a.xml'
            )
        }]
    ),

    (
        (
            'TinderboxPrint: mozharness_revlink: '
            'https://hg.mozilla.org/build/mozharness/rev/16ba958057a8'
        ),
        [{
            'content_type': 'link',
            'title': 'mozharness_revlink',
            'url': 'https://hg.mozilla.org/build/mozharness/rev/16ba958057a8',
            'value': 'https://hg.mozilla.org/build/mozharness/rev/16ba958057a8'
        }]
    ),

    (
        (
            'TinderboxPrint: '
            '<a href=\'http://mozilla-releng-blobs.s3.amazonaws.com'
            '/blobs/cedar/sha512/9123cb277dbf1eb6d90\'>'
            'wpt_structured_full.log'
            '</a>: uploaded'
        ),
        [{
            'content_type': 'link',
            'title': 'artifact uploaded',
            'url': (
                'http://mozilla-releng-blobs.s3.amazonaws.com'
                '/blobs/cedar/sha512/9123cb277dbf1eb6d90'
            ),
            'value': 'wpt_structured_full.log'
        }]
    ),

    (
        (
            'TinderboxPrint: '
            '<a title="libxul_link" href=\''
            'http://graphs.mozilla.org/graph.html#tests=[[205,63,8]]\'>'
            'libxul_link:2918047744'
            '</a>'
        ),
        [{
            'content_type': 'link',
            'title': None,
            'url': 'http://graphs.mozilla.org/graph.html#tests=[[205,63,8]]',
            'value': 'libxul_link:2918047744'
        }]
    ),

    (
        (
            'TinderboxPrint: '
            'xpcshell-xpcshell<br/>2153/<em class="testfail">1</em>&nbsp;'
            '<em class="testfail">CRASH</em>'
        ),
        [{
            'content_type': 'raw_html',
            'title': 'xpcshell-xpcshell',
            'value': (
                '2153/<em class="testfail">1</em>&nbsp;'
                '<em class="testfail">CRASH</em>'
            )
        }]
    ),

    (
        (
            'TinderboxPrint: TalosResult: '
            '{"datazilla": {"tcanvasmark": {"url": '
            '"https://datazilla.mozilla.org?product=Firefox&x86=false'
            '&repository=Try-Non-PGO&os_version=Ubuntu%2012.04'
            '&stop=1406552902&project=talos&start=1405948102'
            '&graph_search=5f51189c6ef8&os=linux&test=tcanvasmark"}, '
            '"tresize": {"url": "https://datazilla.mozilla.org?product'
            '=Firefox&x86=false&repository=Try-Non-PGO&os_version='
            'Ubuntu%2012.04&stop=1406552902&project=talos&start='
            '1405948102&graph_search=5f51189c6ef8&os=linux&test='
            'tcanvasmark&test=tresize"}}, '
            '"graphserver": {"tresize": {"url": '
            '"http://graphs.mozilla.org/graph.html#tests=[[254,113,35]]", '
            '"result": "16.34"}, "tcanvasmark_paint": '
            '{"url": "http://graphs.mozilla.org/graph.html#tests=[[297,113,35]]'
            '", "result": "6807.00"}}}'
        ),
        [{
            'content_type': 'TalosResult',
            'title': 'TalosResult',
            'value': {
                'datazilla': {
                    'tcanvasmark': {
                        'url': ('https://datazilla.mozilla.org?'
                                'product=Firefox&x86=false&repository=Try-Non-PGO'
                                '&os_version=Ubuntu%2012.04&stop=1406552902&'
                                'project=talos&start=1405948102&graph_search='
                                '5f51189c6ef8&os=linux&test=tcanvasmark')
                    },
                    'tresize': {
                        'url': ('https://datazilla.mozilla.org?product=Firefox'
                                '&x86=false&repository=Try-Non-PGO&os_version='
                                'Ubuntu%2012.04&stop=1406552902&project=talos'
                                '&start=1405948102&graph_search=5f51189c6ef8&'
                                'os=linux&test=tcanvasmark&test=tresize')
                    }
                },
                'graphserver': {
                    'tcanvasmark_paint': {
                        'result': '6807.00',
                        'url': ('http://graphs.mozilla.org/graph.html#'
                                'tests=[[297,113,35]]')
                    },
                    'tresize': {
                        'result': '16.34',
                        'url': ('http://graphs.mozilla.org/graph.html#'
                                'tests=[[254,113,35]]')
                    }
                }
            }
        }]
    ),

    (
        (
            'TinderboxPrint: hazard results: '
            'https://ftp-ssl.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/'
            'mozilla-central-linux64-br-haz/20150226025813'
        ),
        [{
            'content_type': 'link',
            'title': 'hazard results',
            'url': 'https://ftp-ssl.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/'
                   'mozilla-central-linux64-br-haz/20150226025813',
            'value': 'https://ftp-ssl.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/'
                     'mozilla-central-linux64-br-haz/20150226025813'
        }]
    ),
)


@pytest.mark.parametrize(("line", "artifact"), TINDERBOX_TEST_CASES)
def test_tinderbox_parser_output(line, artifact):
    parser = TinderboxPrintParser()
    parser.parse_line(line, 1)

    assert artifact == parser.get_artifact()


def test_invalid_talosresult():
    invalid_line = 'TinderboxPrint: TalosResult: foo{bar}'
    parser = TinderboxPrintParser()
    with pytest.raises(ValueError):
        parser.parse_line(invalid_line, 1)
