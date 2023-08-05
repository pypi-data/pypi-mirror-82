import ezissue.ezissue as ezissue


def test_md_table_row_to_array():
    md = '| get to the choppa | asdf | jkl |'
    array = ezissue.md_table_row_to_array(md)

    md2 = '|get to the choppa|asdf|jkl|'
    array2 = ezissue.md_table_row_to_array(md2)

    if not array == ['get to the choppa', 'asdf', 'jkl']:
        raise AssertionError()

    if not array2 == ['get to the choppa', 'asdf', 'jkl']:
        raise AssertionError()


def test_add_md_checkbox():
    arg = "as ioajdioa jsdf;asdf;adsf;asdf"
    resp = ezissue.add_md_checkbox(arg)

    if not (resp == '- [ ] As ioajdioa jsdf\n- [ ] Asdf\n- [ ] Adsf\n- [ ] Asdf\n'):
        raise AssertionError()


def test_format_description():
    desc = "lorem ipsum dolor sit amet"
    a = ezissue.format_description(desc)

    if not (
        a == '**Issue description:**\n---\n\nlorem ipsum dolor sit amet\n\n'):
        raise AssertionError()


def test_add_prefix_to_title():
    titles = ["make america great again", "make stuff work"]
    formattedUS = []
    formattedTS = []

    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'US', '', True))
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'TS', '', True))
    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'US', 'M', False))
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, 'TS', 'M', False))
    for idx, title in enumerate(titles):
        formattedUS.append(
            ezissue.add_prefix_to_title(title, idx+1, '', '', False))
        formattedTS.append(
            ezissue.add_prefix_to_title(title, idx+1, '', '', False))

    if not (formattedUS[0] == 'US1 Make america great again' and formattedTS[0] == 'TS1 Make america great again'):
        raise AssertionError()

    if not (formattedUS[1] == 'US2 Make stuff work' and formattedTS[1] == 'TS2 Make stuff work'):
        raise AssertionError()

    if not (formattedUS[2] == 'USM Make america great again' and formattedTS[2] == 'TSM Make america great again'):
        raise AssertionError()

    if not (formattedUS[3] == 'USM Make stuff work' and formattedTS[3] == 'TSM Make stuff work'):
        raise AssertionError()

    if not (formattedUS[4] == ' Make america great again' and formattedTS[4] == ' Make america great again'):
        raise AssertionError()

    if not (formattedUS[5] == ' Make stuff work' and formattedTS[5] == ' Make stuff work'):
        raise AssertionError()


def test_create_github_url():
    url = ezissue.create_github_url('commit-helper', 'andre-filho')
    expected = "https://api.github.com/repos/andre-filho/commit-helper/issues"

    if not url == expected:
        raise AssertionError()


def test_create_gitlab_url():
    url = ezissue.create_gitlab_url(1234)
    expected = "https://gitlab.com/api/v4/projects/1234/issues"

    if not url == expected:
        raise AssertionError()


def test_get_table_spec():
    length_thead, thead = ezissue.get_table_spec('| asdfds | asdf | asdf |')
    length_thead2, thead2 = ezissue.get_table_spec('|asdfds|asdf|asdf|')
    length_thead3, thead3 = ezissue.get_table_spec('|Asdfds|Asdf|Asdf|')

    if not length_thead == 3:
        raise AssertionError()

    if not thead == ['asdfds', 'asdf', 'asdf']:
        raise AssertionError()

    if not length_thead2 == 3:
        raise AssertionError()

    if not thead2 == ['asdfds', 'asdf', 'asdf']:
        raise AssertionError()

    if not length_thead3 == 3:
        raise AssertionError()

    if not thead3 == ['asdfds', 'asdf', 'asdf']:
        raise AssertionError()


def test_create_issue_json():
    a = ezissue.create_issue_json(
        ['title', 'description', 'accept'],
        [[1], 2, 3],
        'github'
    )
    b = ezissue.create_issue_json(
        ['title', 'body', 'accept'],
        [[1], 2, 3],
        'gitlab'
    )
