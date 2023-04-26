from typer.testing import CliRunner
import os
import json
import pytest
from besecure_developer_toolkit.cli import app
from unittest.mock import patch
from unittest.mock import Mock
from besecure_developer_toolkit.src.create_ossp_master import OSSPMaster

runner = CliRunner()

@pytest.fixture
def ossp_master_fixture():
    """fixture function for declaring common variables.

    Yields:
        class obj: OSSPMaster Class
    """
    issue_id = 136
    name = "fastjson"
    obj = OSSPMaster(issue_id, name)
    yield obj


def test_check_issue_exists(ossp_master_fixture):
    """Test OSSPMaster.check_issue_exists
    """
    with patch('besecure_developer_toolkit.src.CreateOsspMaster.requests.head') as mock_requests:
        mock_response = mock_requests.return_value
        mock_response.status_code = 200
        url = f"https://github.com/Be-Secure/Be-Secure/issues/{ossp_master_fixture.issue_id}"
        assert OSSPMaster.check_issue_exists(ossp_master_fixture.issue_id) is True
        mock_requests.assert_called_once_with(url)

def test_check_repo_exists(ossp_master_fixture):
    with patch('besecure_developer_toolkit.src.CreateOsspMaster.requests.head') as mock_requests:
        mock_response = mock_requests.return_value
        mock_response.status_code = 200
        url = f"https://github.com/Be-Secure/Be-Secure/{ossp_master_fixture.name}"
        assert OSSPMaster.check_repo_exists(ossp_master_fixture.name) == True
        mock_requests.assert_called_once_with(url)

def test_id_project_mismatch(ossp_master_fixture):
    with patch('besecure_developer_toolkit.src.CreateOsspMaster.urlopen') as mock_urlopen:
        mock_data = {'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136', 'repository_url': 'https://api.github.com/repos/Be-Secure/Be-Secure', 'labels_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/labels{/name}', 'comments_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/comments', 'events_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/events', 'html_url': 'https://github.com/Be-Secure/Be-Secure/issues/136', 'issue_id': 1615030821, 'node_id': 'I_kwDOCkfhIc5gQ2ol', 'number': 136, 'title': 'TAVOSS-TR: fastjson', 'user': {'login': 'vasanthtech', 'issue_id': 103616400, 'node_id': 'U_kgDOBi0PkA', 'avatar_url': 'https://avatars.githubusercontent.com/u/103616400?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/vasanthtech', 'html_url': 'https://github.com/vasanthtech', 'followers_url': 'https://api.github.com/users/vasanthtech/followers', 'following_url': 'https://api.github.com/users/vasanthtech/following{/other_user}', 'gists_url': 'https://api.github.com/users/vasanthtech/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/vasanthtech/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/vasanthtech/subscriptions', 'organizations_url': 'https://api.github.com/users/vasanthtech/orgs', 'repos_url': 'https://api.github.com/users/vasanthtech/repos', 'events_url': 'https://api.github.com/users/vasanthtech/events{/privacy}', 'received_events_url': 'https://api.github.com/users/vasanthtech/received_events', 'type': 'User', 'site_admin': False}, 'labels': [{'issue_id': 5239729079, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_rtw', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/COM%20-%20C', 'name': 'COM - C', 'color': '69c3d7', 'default': False, 'description': None}, {'issue_id': 5239729093, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_rxQ', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/IND-ALL', 'name': 'IND-ALL', 'color': '7030a0', 'default': False, 'description': None}, {'issue_id': 5239729136, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_r8A', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/L&F', 'name': 'L&F', 'color': 'ffff00', 'default': False, 'description': None}, {'issue_id': 5239729184, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_sIA', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/Tracked', 'name': 'Tracked', 'color': '2FC2EB', 'default': False, 'description': None}], 'state': 'open', 'locked': False, 'assignee': None, 'assignees': [{'login': 'asa1997', 'issue_id': 58501088, 'node_id': 'MDQ6VXNlcjU4NTAxMDg4', 'avatar_url': 'https://avatars.githubusercontent.com/u/58501088?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/asa1997', 'html_url': 'https://github.com/asa1997', 'followers_url': 'https://api.github.com/users/asa1997/followers', 'following_url': 'https://api.github.com/users/asa1997/following{/other_user}', 'gists_url': 'https://api.github.com/users/asa1997/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/asa1997/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/asa1997/subscriptions', 'organizations_url': 'https://api.github.com/users/asa1997/orgs', 'repos_url': 'https://api.github.com/users/asa1997/repos', 'events_url': 'https://api.github.com/users/asa1997/events{/privacy}', 'received_events_url': 'https://api.github.com/users/asa1997/received_events', 'type': 'User', 'site_admin': False}], 'milestone': None, 'comments': 0, 'created_at': '2022-07-20T07:31:43Z', 'updated_at': '2023-03-29T11:07:57Z', 'closed_at': None, 'author_association': 'NONE', 'active_lock_reason': None, 'body': '### Version of the project\r\n\r\n1.2.24\r\n\r\n### Tech Stack\r\n\r\nLanguage and Framwork [L&F]\r\n\r\n### Project details\r\n\r\nFastjson is a Java library that can be used to convert Java Objects into their JSON representation. It can also be used to convert a JSON string to an equivalent Java object. Fastjson can work with arbitrary Java objects including pre-existing objects that you do not have source-code of.\r\n\r\nFastjson Goals\r\n\r\n    Provide the best performance on the server-side and android client\r\n    Provide simple toJSONString() and parseObject() methods to convert Java objects to JSON and vice-versa\r\n    Allow pre-existing unmodifiable objects to be converted to and from JSON\r\n    Extensive support of Java Generics\r\n    Allow custom representations for objects\r\n    Support arbitrarily complex objects (with deep inheritance hierarchies and extensive use of generic types)\r\n\r\n\r\n### Languages used\r\n\r\nJava \r\n\r\n### Domain\r\n\r\nWeb Development\r\n\r\n### Industry\r\n\r\nAll\r\n\r\n### Open Source Project type\r\n\r\nCommunity led\r\n\r\n### Repo URL\r\n\r\nhttps://github.com/alibaba/fastjson.git\r\n\r\n### Sub-project repo URL\r\n\r\n_No response_\r\n\r\n### Webpage\r\n\r\n_No response_\r\n\r\n### License\r\n\r\nApache-2.0\r\n\r\n### Other license\r\n\r\n_No response_\r\n\r\n### Reason , why we must track this project.\r\n', 'closed_by': None, 'reactions': {'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/reactions', 'total_count': 0, '+1': 0, '-1': 0, 'laugh': 0, 'hooray': 0, 'confused': 0, 'heart': 0, 'rocket': 0, 'eyes': 0}, 'timeline_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/timeline', 'performed_via_github_app': None, 'state_reason': None}
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value = mock_response
        result = OSSPMaster.check_issue_related_to_project(ossp_master_fixture)
        assert result == True

def test_write_tech_stack(ossp_master_fixture):
    expected = "L&F"
    with patch('besecure_developer_toolkit.src.CreateOsspMaster.urlopen') as mock_urlopen:
        mock_data = {'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136', 'repository_url': 'https://api.github.com/repos/Be-Secure/Be-Secure', 'labels_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/labels{/name}', 'comments_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/comments', 'events_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/events', 'html_url': 'https://github.com/Be-Secure/Be-Secure/issues/136', 'issue_id': 1615030821, 'node_id': 'I_kwDOCkfhIc5gQ2ol', 'number': 136, 'title': 'TAVOSS-TR: fastjson', 'user': {'login': 'vasanthtech', 'issue_id': 103616400, 'node_id': 'U_kgDOBi0PkA', 'avatar_url': 'https://avatars.githubusercontent.com/u/103616400?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/vasanthtech', 'html_url': 'https://github.com/vasanthtech', 'followers_url': 'https://api.github.com/users/vasanthtech/followers', 'following_url': 'https://api.github.com/users/vasanthtech/following{/other_user}', 'gists_url': 'https://api.github.com/users/vasanthtech/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/vasanthtech/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/vasanthtech/subscriptions', 'organizations_url': 'https://api.github.com/users/vasanthtech/orgs', 'repos_url': 'https://api.github.com/users/vasanthtech/repos', 'events_url': 'https://api.github.com/users/vasanthtech/events{/privacy}', 'received_events_url': 'https://api.github.com/users/vasanthtech/received_events', 'type': 'User', 'site_admin': False}, 'labels': [{'issue_id': 5239729079, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_rtw', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/COM%20-%20C', 'name': 'COM - C', 'color': '69c3d7', 'default': False, 'description': None}, {'issue_id': 5239729093, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_rxQ', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/IND-ALL', 'name': 'IND-ALL', 'color': '7030a0', 'default': False, 'description': None}, {'issue_id': 5239729136, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_r8A', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/L&F', 'name': 'L&F', 'color': 'ffff00', 'default': False, 'description': None}, {'issue_id': 5239729184, 'node_id': 'LA_kwDOCkfhIc8AAAABOE_sIA', 'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/labels/Tracked', 'name': 'Tracked', 'color': '2FC2EB', 'default': False, 'description': None}], 'state': 'open', 'locked': False, 'assignee': None, 'assignees': [{'login': 'asa1997', 'issue_id': 58501088, 'node_id': 'MDQ6VXNlcjU4NTAxMDg4', 'avatar_url': 'https://avatars.githubusercontent.com/u/58501088?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/asa1997', 'html_url': 'https://github.com/asa1997', 'followers_url': 'https://api.github.com/users/asa1997/followers', 'following_url': 'https://api.github.com/users/asa1997/following{/other_user}', 'gists_url': 'https://api.github.com/users/asa1997/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/asa1997/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/asa1997/subscriptions', 'organizations_url': 'https://api.github.com/users/asa1997/orgs', 'repos_url': 'https://api.github.com/users/asa1997/repos', 'events_url': 'https://api.github.com/users/asa1997/events{/privacy}', 'received_events_url': 'https://api.github.com/users/asa1997/received_events', 'type': 'User', 'site_admin': False}], 'milestone': None, 'comments': 0, 'created_at': '2022-07-20T07:31:43Z', 'updated_at': '2023-03-29T11:07:57Z', 'closed_at': None, 'author_association': 'NONE', 'active_lock_reason': None, 'body': '### Version of the project\r\n\r\n1.2.24\r\n\r\n### Tech Stack\r\n\r\nLanguage and Framwork [L&F]\r\n\r\n### Project details\r\n\r\nFastjson is a Java library that can be used to convert Java Objects into their JSON representation. It can also be used to convert a JSON string to an equivalent Java object. Fastjson can work with arbitrary Java objects including pre-existing objects that you do not have source-code of.\r\n\r\nFastjson Goals\r\n\r\n    Provide the best performance on the server-side and android client\r\n    Provide simple toJSONString() and parseObject() methods to convert Java objects to JSON and vice-versa\r\n    Allow pre-existing unmodifiable objects to be converted to and from JSON\r\n    Extensive support of Java Generics\r\n    Allow custom representations for objects\r\n    Support arbitrarily complex objects (with deep inheritance hierarchies and extensive use of generic types)\r\n\r\n\r\n### Languages used\r\n\r\nJava \r\n\r\n### Domain\r\n\r\nWeb Development\r\n\r\n### Industry\r\n\r\nAll\r\n\r\n### Open Source Project type\r\n\r\nCommunity led\r\n\r\n### Repo URL\r\n\r\nhttps://github.com/alibaba/fastjson.git\r\n\r\n### Sub-project repo URL\r\n\r\n_No response_\r\n\r\n### Webpage\r\n\r\n_No response_\r\n\r\n### License\r\n\r\nApache-2.0\r\n\r\n### Other license\r\n\r\n_No response_\r\n\r\n### Reason , why we must track this project.\r\n', 'closed_by': None, 'reactions': {'url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/reactions', 'total_count': 0, '+1': 0, '-1': 0, 'laugh': 0, 'hooray': 0, 'confused': 0, 'heart': 0, 'rocket': 0, 'eyes': 0}, 'timeline_url': 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/136/timeline', 'performed_via_github_app': None, 'state_reason': None}
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(mock_data).encode()
        mock_urlopen.return_value = mock_response
        result = OSSPMaster.write_tech_stack(ossp_master_fixture.issue_id)
        assert result == expected

def test_write_project_repos_data(ossp_master_fixture):
    data = {
        "main_github_url": "https://github.com/alibaba/fastjson",
        "main_bes_url": "https://github.com/Be-Secure/fastjson",
        "all_projects": {
          "fastjson": "https://github.com/alibaba/fastjson"
        },
        "all_bes_repos": [
          {
            "issue_id": 498655991,
            "name": "fastjson",
            "url": "https://github.com/Be-Secure/fastjson"
          }
        ]
    }
    expected = json.dumps(data)
    mock_data = {'issue_id': 498655991, 'node_id': 'R_kgDOHbji9w', 'name': 'fastjson', 'full_name': 'Be-Secure/fastjson', 'private': False, 'owner': {'login': 'Be-Secure', 'issue_id': 44028837, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjQ0MDI4ODM3', 'avatar_url': 'https://avatars.githubusercontent.com/u/44028837?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Be-Secure', 'html_url': 'https://github.com/Be-Secure', 'followers_url': 'https://api.github.com/users/Be-Secure/followers', 'following_url': 'https://api.github.com/users/Be-Secure/following{/other_user}', 'gists_url': 'https://api.github.com/users/Be-Secure/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Be-Secure/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/Be-Secure/subscriptions', 'organizations_url': 'https://api.github.com/users/Be-Secure/orgs', 'repos_url': 'https://api.github.com/users/Be-Secure/repos', 'events_url': 'https://api.github.com/users/Be-Secure/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Be-Secure/received_events', 'type': 'Organization', 'site_admin': False}, 'html_url': 'https://github.com/Be-Secure/fastjson', 'description': 'A fast JSON parser/generator for Java.  ', 'fork': True, 'url': 'https://api.github.com/repos/Be-Secure/fastjson', 'forks_url': 'https://api.github.com/repos/Be-Secure/fastjson/forks', 'keys_url': 'https://api.github.com/repos/Be-Secure/fastjson/keys{/key_id}', 'collaborators_url': 'https://api.github.com/repos/Be-Secure/fastjson/collaborators{/collaborator}', 'teams_url': 'https://api.github.com/repos/Be-Secure/fastjson/teams', 'hooks_url': 'https://api.github.com/repos/Be-Secure/fastjson/hooks', 'issue_events_url': 'https://api.github.com/repos/Be-Secure/fastjson/issues/events{/number}', 'events_url': 'https://api.github.com/repos/Be-Secure/fastjson/events', 'assignees_url': 'https://api.github.com/repos/Be-Secure/fastjson/assignees{/user}', 'branches_url': 'https://api.github.com/repos/Be-Secure/fastjson/branches{/branch}', 'tags_url': 'https://api.github.com/repos/Be-Secure/fastjson/tags', 'blobs_url': 'https://api.github.com/repos/Be-Secure/fastjson/git/blobs{/sha}', 'git_tags_url': 'https://api.github.com/repos/Be-Secure/fastjson/git/tags{/sha}', 'git_refs_url': 'https://api.github.com/repos/Be-Secure/fastjson/git/refs{/sha}', 'trees_url': 'https://api.github.com/repos/Be-Secure/fastjson/git/trees{/sha}', 'statuses_url': 'https://api.github.com/repos/Be-Secure/fastjson/statuses/{sha}', 'languages_url': 'https://api.github.com/repos/Be-Secure/fastjson/languages', 'stargazers_url': 'https://api.github.com/repos/Be-Secure/fastjson/stargazers', 'contributors_url': 'https://api.github.com/repos/Be-Secure/fastjson/contributors', 'subscribers_url': 'https://api.github.com/repos/Be-Secure/fastjson/subscribers', 'subscription_url': 'https://api.github.com/repos/Be-Secure/fastjson/subscription', 'commits_url': 'https://api.github.com/repos/Be-Secure/fastjson/commits{/sha}', 'git_commits_url': 'https://api.github.com/repos/Be-Secure/fastjson/git/commits{/sha}', 'comments_url': 'https://api.github.com/repos/Be-Secure/fastjson/comments{/number}', 'issue_comment_url': 'https://api.github.com/repos/Be-Secure/fastjson/issues/comments{/number}', 'contents_url': 'https://api.github.com/repos/Be-Secure/fastjson/contents/{+path}', 'compare_url': 'https://api.github.com/repos/Be-Secure/fastjson/compare/{base}...{head}', 'merges_url': 'https://api.github.com/repos/Be-Secure/fastjson/merges', 'archive_url': 'https://api.github.com/repos/Be-Secure/fastjson/{archive_format}{/ref}', 'downloads_url': 'https://api.github.com/repos/Be-Secure/fastjson/downloads', 'issues_url': 'https://api.github.com/repos/Be-Secure/fastjson/issues{/number}', 'pulls_url': 'https://api.github.com/repos/Be-Secure/fastjson/pulls{/number}', 'milestones_url': 'https://api.github.com/repos/Be-Secure/fastjson/milestones{/number}', 'notifications_url': 'https://api.github.com/repos/Be-Secure/fastjson/notifications{?since,all,participating}', 'labels_url': 'https://api.github.com/repos/Be-Secure/fastjson/labels{/name}', 'releases_url': 'https://api.github.com/repos/Be-Secure/fastjson/releases{/issue_id}', 'deployments_url': 'https://api.github.com/repos/Be-Secure/fastjson/deployments', 'created_at': '2022-06-01T08:40:32Z', 'updated_at': '2022-06-20T05:16:20Z', 'pushed_at': '2023-02-08T09:24:35Z', 'git_url': 'git://github.com/Be-Secure/fastjson.git', 'ssh_url': 'git@github.com:Be-Secure/fastjson.git', 'clone_url': 'https://github.com/Be-Secure/fastjson.git', 'svn_url': 'https://github.com/Be-Secure/fastjson', 'homepage': 'https://github.com/alibaba/fastjson/wiki', 'size': 15488, 'stargazers_count': 0, 'watchers_count': 0, 'language': 'Java', 'has_issues': False, 'has_projects': True, 'has_downloads': True, 'has_wiki': True, 'has_pages': False, 'has_discussions': False, 'forks_count': 0, 'mirror_url': None, 'archived': False, 'disabled': False, 'open_issues_count': 0, 'license': {'key': 'other', 'name': 'Other', 'spdx_id': 'NOASSERTION', 'url': None, 'node_id': 'MDc6TGljZW5zZTA='}, 'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False, 'topics': [], 'visibility': 'public', 'forks': 0, 'open_issues': 0, 'watchers': 0, 'default_branch': '1.2.24_release', 'temp_clone_token': None, 'organization': {'login': 'Be-Secure', 'issue_id': 44028837, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjQ0MDI4ODM3', 'avatar_url': 'https://avatars.githubusercontent.com/u/44028837?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Be-Secure', 'html_url': 'https://github.com/Be-Secure', 'followers_url': 'https://api.github.com/users/Be-Secure/followers', 'following_url': 'https://api.github.com/users/Be-Secure/following{/other_user}', 'gists_url': 'https://api.github.com/users/Be-Secure/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Be-Secure/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/Be-Secure/subscriptions', 'organizations_url': 'https://api.github.com/users/Be-Secure/orgs', 'repos_url': 'https://api.github.com/users/Be-Secure/repos', 'events_url': 'https://api.github.com/users/Be-Secure/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Be-Secure/received_events', 'type': 'Organization', 'site_admin': False}, 'parent': {'issue_id': 2700474, 'node_id': 'MDEwOlJlcG9zaXRvcnkyNzAwNDc0', 'name': 'fastjson', 'full_name': 'alibaba/fastjson', 'private': False, 'owner': {'login': 'alibaba', 'issue_id': 1961952, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjE5NjE5NTI=', 'avatar_url': 'https://avatars.githubusercontent.com/u/1961952?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/alibaba', 'html_url': 'https://github.com/alibaba', 'followers_url': 'https://api.github.com/users/alibaba/followers', 'following_url': 'https://api.github.com/users/alibaba/following{/other_user}', 'gists_url': 'https://api.github.com/users/alibaba/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/alibaba/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/alibaba/subscriptions', 'organizations_url': 'https://api.github.com/users/alibaba/orgs', 'repos_url': 'https://api.github.com/users/alibaba/repos', 'events_url': 'https://api.github.com/users/alibaba/events{/privacy}', 'received_events_url': 'https://api.github.com/users/alibaba/received_events', 'type': 'Organization', 'site_admin': False}, 'html_url': 'https://github.com/alibaba/fastjson', 'description': 'FASTJSON 2.0.x has been released, faster and more secure, recommend you upgrade.', 'fork': False, 'url': 'https://api.github.com/repos/alibaba/fastjson', 'forks_url': 'https://api.github.com/repos/alibaba/fastjson/forks', 'keys_url': 'https://api.github.com/repos/alibaba/fastjson/keys{/key_id}', 'collaborators_url': 'https://api.github.com/repos/alibaba/fastjson/collaborators{/collaborator}', 'teams_url': 'https://api.github.com/repos/alibaba/fastjson/teams', 'hooks_url': 'https://api.github.com/repos/alibaba/fastjson/hooks', 'issue_events_url': 'https://api.github.com/repos/alibaba/fastjson/issues/events{/number}', 'events_url': 'https://api.github.com/repos/alibaba/fastjson/events', 'assignees_url': 'https://api.github.com/repos/alibaba/fastjson/assignees{/user}', 'branches_url': 'https://api.github.com/repos/alibaba/fastjson/branches{/branch}', 'tags_url': 'https://api.github.com/repos/alibaba/fastjson/tags', 'blobs_url': 'https://api.github.com/repos/alibaba/fastjson/git/blobs{/sha}', 'git_tags_url': 'https://api.github.com/repos/alibaba/fastjson/git/tags{/sha}', 'git_refs_url': 'https://api.github.com/repos/alibaba/fastjson/git/refs{/sha}', 'trees_url': 'https://api.github.com/repos/alibaba/fastjson/git/trees{/sha}', 'statuses_url': 'https://api.github.com/repos/alibaba/fastjson/statuses/{sha}', 'languages_url': 'https://api.github.com/repos/alibaba/fastjson/languages', 'stargazers_url': 'https://api.github.com/repos/alibaba/fastjson/stargazers', 'contributors_url': 'https://api.github.com/repos/alibaba/fastjson/contributors', 'subscribers_url': 'https://api.github.com/repos/alibaba/fastjson/subscribers', 'subscription_url': 'https://api.github.com/repos/alibaba/fastjson/subscription', 'commits_url': 'https://api.github.com/repos/alibaba/fastjson/commits{/sha}', 'git_commits_url': 'https://api.github.com/repos/alibaba/fastjson/git/commits{/sha}', 'comments_url': 'https://api.github.com/repos/alibaba/fastjson/comments{/number}', 'issue_comment_url': 'https://api.github.com/repos/alibaba/fastjson/issues/comments{/number}', 'contents_url': 'https://api.github.com/repos/alibaba/fastjson/contents/{+path}', 'compare_url': 'https://api.github.com/repos/alibaba/fastjson/compare/{base}...{head}', 'merges_url': 'https://api.github.com/repos/alibaba/fastjson/merges', 'archive_url': 'https://api.github.com/repos/alibaba/fastjson/{archive_format}{/ref}', 'downloads_url': 'https://api.github.com/repos/alibaba/fastjson/downloads', 'issues_url': 'https://api.github.com/repos/alibaba/fastjson/issues{/number}', 'pulls_url': 'https://api.github.com/repos/alibaba/fastjson/pulls{/number}', 'milestones_url': 'https://api.github.com/repos/alibaba/fastjson/milestones{/number}', 'notifications_url': 'https://api.github.com/repos/alibaba/fastjson/notifications{?since,all,participating}', 'labels_url': 'https://api.github.com/repos/alibaba/fastjson/labels{/name}', 'releases_url': 'https://api.github.com/repos/alibaba/fastjson/releases{/issue_id}', 'deployments_url': 'https://api.github.com/repos/alibaba/fastjson/deployments', 'created_at': '2011-11-03T06:58:52Z', 'updated_at': '2023-04-25T06:39:10Z', 'pushed_at': '2023-04-20T01:26:18Z', 'git_url': 'git://github.com/alibaba/fastjson.git', 'ssh_url': 'git@github.com:alibaba/fastjson.git', 'clone_url': 'https://github.com/alibaba/fastjson.git', 'svn_url': 'https://github.com/alibaba/fastjson', 'homepage': 'https://github.com/alibaba/fastjson2/wiki/fastjson_1_upgrade_cn', 'size': 15512, 'stargazers_count': 25293, 'watchers_count': 25293, 'language': 'Java', 'has_issues': True, 'has_projects': False, 'has_downloads': True, 'has_wiki': True, 'has_pages': False, 'has_discussions': False, 'forks_count': 6526, 'mirror_url': None, 'archived': False, 'disabled': False, 'open_issues_count': 1991, 'license': {'key': 'apache-2.0', 'name': 'Apache License 2.0', 'spdx_id': 'Apache-2.0', 'url': 'https://api.github.com/licenses/apache-2.0', 'node_id': 'MDc6TGljZW5zZTI='}, 'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False, 'topics': ['android', 'best-performance', 'deserialization', 'fastjson', 'java', 'json', 'json-parser', 'json-serialization', 'json-serializer', 'serialization'], 'visibility': 'public', 'forks': 6526, 'open_issues': 1991, 'watchers': 25293, 'default_branch': 'master'}, 'source': {'issue_id': 2700474, 'node_id': 'MDEwOlJlcG9zaXRvcnkyNzAwNDc0', 'name': 'fastjson', 'full_name': 'alibaba/fastjson', 'private': False, 'owner': {'login': 'alibaba', 'issue_id': 1961952, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjE5NjE5NTI=', 'avatar_url': 'https://avatars.githubusercontent.com/u/1961952?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/alibaba', 'html_url': 'https://github.com/alibaba', 'followers_url': 'https://api.github.com/users/alibaba/followers', 'following_url': 'https://api.github.com/users/alibaba/following{/other_user}', 'gists_url': 'https://api.github.com/users/alibaba/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/alibaba/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/alibaba/subscriptions', 'organizations_url': 'https://api.github.com/users/alibaba/orgs', 'repos_url': 'https://api.github.com/users/alibaba/repos', 'events_url': 'https://api.github.com/users/alibaba/events{/privacy}', 'received_events_url': 'https://api.github.com/users/alibaba/received_events', 'type': 'Organization', 'site_admin': False}, 'html_url': 'https://github.com/alibaba/fastjson', 'description': 'FASTJSON 2.0.x has been released, faster and more secure, recommend you upgrade.', 'fork': False, 'url': 'https://api.github.com/repos/alibaba/fastjson', 'forks_url': 'https://api.github.com/repos/alibaba/fastjson/forks', 'keys_url': 'https://api.github.com/repos/alibaba/fastjson/keys{/key_id}', 'collaborators_url': 'https://api.github.com/repos/alibaba/fastjson/collaborators{/collaborator}', 'teams_url': 'https://api.github.com/repos/alibaba/fastjson/teams', 'hooks_url': 'https://api.github.com/repos/alibaba/fastjson/hooks', 'issue_events_url': 'https://api.github.com/repos/alibaba/fastjson/issues/events{/number}', 'events_url': 'https://api.github.com/repos/alibaba/fastjson/events', 'assignees_url': 'https://api.github.com/repos/alibaba/fastjson/assignees{/user}', 'branches_url': 'https://api.github.com/repos/alibaba/fastjson/branches{/branch}', 'tags_url': 'https://api.github.com/repos/alibaba/fastjson/tags', 'blobs_url': 'https://api.github.com/repos/alibaba/fastjson/git/blobs{/sha}', 'git_tags_url': 'https://api.github.com/repos/alibaba/fastjson/git/tags{/sha}', 'git_refs_url': 'https://api.github.com/repos/alibaba/fastjson/git/refs{/sha}', 'trees_url': 'https://api.github.com/repos/alibaba/fastjson/git/trees{/sha}', 'statuses_url': 'https://api.github.com/repos/alibaba/fastjson/statuses/{sha}', 'languages_url': 'https://api.github.com/repos/alibaba/fastjson/languages', 'stargazers_url': 'https://api.github.com/repos/alibaba/fastjson/stargazers', 'contributors_url': 'https://api.github.com/repos/alibaba/fastjson/contributors', 'subscribers_url': 'https://api.github.com/repos/alibaba/fastjson/subscribers', 'subscription_url': 'https://api.github.com/repos/alibaba/fastjson/subscription', 'commits_url': 'https://api.github.com/repos/alibaba/fastjson/commits{/sha}', 'git_commits_url': 'https://api.github.com/repos/alibaba/fastjson/git/commits{/sha}', 'comments_url': 'https://api.github.com/repos/alibaba/fastjson/comments{/number}', 'issue_comment_url': 'https://api.github.com/repos/alibaba/fastjson/issues/comments{/number}', 'contents_url': 'https://api.github.com/repos/alibaba/fastjson/contents/{+path}', 'compare_url': 'https://api.github.com/repos/alibaba/fastjson/compare/{base}...{head}', 'merges_url': 'https://api.github.com/repos/alibaba/fastjson/merges', 'archive_url': 'https://api.github.com/repos/alibaba/fastjson/{archive_format}{/ref}', 'downloads_url': 'https://api.github.com/repos/alibaba/fastjson/downloads', 'issues_url': 'https://api.github.com/repos/alibaba/fastjson/issues{/number}', 'pulls_url': 'https://api.github.com/repos/alibaba/fastjson/pulls{/number}', 'milestones_url': 'https://api.github.com/repos/alibaba/fastjson/milestones{/number}', 'notifications_url': 'https://api.github.com/repos/alibaba/fastjson/notifications{?since,all,participating}', 'labels_url': 'https://api.github.com/repos/alibaba/fastjson/labels{/name}', 'releases_url': 'https://api.github.com/repos/alibaba/fastjson/releases{/issue_id}', 'deployments_url': 'https://api.github.com/repos/alibaba/fastjson/deployments', 'created_at': '2011-11-03T06:58:52Z', 'updated_at': '2023-04-25T06:39:10Z', 'pushed_at': '2023-04-20T01:26:18Z', 'git_url': 'git://github.com/alibaba/fastjson.git', 'ssh_url': 'git@github.com:alibaba/fastjson.git', 'clone_url': 'https://github.com/alibaba/fastjson.git', 'svn_url': 'https://github.com/alibaba/fastjson', 'homepage': 'https://github.com/alibaba/fastjson2/wiki/fastjson_1_upgrade_cn', 'size': 15512, 'stargazers_count': 25293, 'watchers_count': 25293, 'language': 'Java', 'has_issues': True, 'has_projects': False, 'has_downloads': True, 'has_wiki': True, 'has_pages': False, 'has_discussions': False, 'forks_count': 6526, 'mirror_url': None, 'archived': False, 'disabled': False, 'open_issues_count': 1991, 'license': {'key': 'apache-2.0', 'name': 'Apache License 2.0', 'spdx_id': 'Apache-2.0', 'url': 'https://api.github.com/licenses/apache-2.0', 'node_id': 'MDc6TGljZW5zZTI='}, 'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False, 'topics': ['android', 'best-performance', 'deserialization', 'fastjson', 'java', 'json', 'json-parser', 'json-serialization', 'json-serializer', 'serialization'], 'visibility': 'public', 'forks': 6526, 'open_issues': 1991, 'watchers': 25293, 'default_branch': 'master'}, 'network_count': 6526, 'subscribers_count': 0}
    mock_response = Mock()
    mock_response.read.return_value = json.dumps(mock_data)
    result = OSSPMaster.write_project_repos_data(json.dumps(mock_data))
    assert result == expected

def test_metadata():
    issue_id = "136"
    name = "fastjson"
    version = "version"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=issue_id+"\n"+name+"\n")
    assert result.exit_code == 0
    version_file = os.path.exists(f'{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json')
    ossp_master_file = os.path.exists(f'{osspoi}/OSSP-Master.json')
    print(ossp_master_file)
    f = open(f'{osspoi}/OSSP-Master.json')
    ossp_master_data = json.load(f)
    for i in range(len(ossp_master_data["items"])):
        if ossp_master_data["items"][i]["issue_id"] == int(issue_id) and ossp_master_data["items"][i]["name"] == name:
            found = True
            break
        else:
            found = False
    assert ossp_master_file == True
    assert version_file == True
    assert found == True

def test_version_file_not_empty():
    issue_id = "136"
    name = "fastjson"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=issue_id+"\n"+name+"\n")
    assert result.exit_code == 0
    size = os.path.getsize(f'{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json')
    assert size > 0

def test_overwrite():
    issue_id = "136"
    name = "fastjson"
    version = "1.2.24"
    test_version_file = [{
        "version": "1.2.24",
        "release_date": "19-Jan-2017",
        "criticality_score": "Not Available",
        "scorecard": "Not Available",
        "cve_details": "Not Available"
    }]
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata", "--overwrite"], input=issue_id+"\n"+name+"\n")
    assert result.exit_code == 0
    f = open(f'{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json')
    fastjson_version_file = json.load(f)
    assert sorted(test_version_file[0]) == sorted(fastjson_version_file[0])

def test_without_overwrite():
    issue_id = "136"
    name = "fastjson"
    version = "1.2.24"
    osspoi = os.environ['OSSPOI_DIR']
    f = open(f"{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json")
    original_version_data = json.load(f)
    for i in range(len(original_version_data)):
        if original_version_data[i]["version"] == version:
            test_data_original = original_version_data[i]
            break
    f.close()
    result = runner.invoke(app, ["generate", "metadata"], input=issue_id+"\n"+name+"\n")
    f = open(f"{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json")
    original_version_data = json.load(f)
    for i in range(len(original_version_data)):
        if original_version_data[i]["version"] == version:
            test_data_new = original_version_data[i]
            break
    f.close()
    assert result.exit_code == 0
    assert sorted(test_data_original) == sorted(test_data_new)
    assert f'Alert! Entry for {issue_id}-{name} already present' in result.stdout
    assert f'Alert! Version {version} exists' in result.stdout

def test_issue_project_mismatch():
    issue_id = 137
    name = "fastjson"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=str(issue_id)+"\n"+name+"\n")
    assert result.exit_code == 0
    f = open(f'{osspoi}/OSSP-Master.json')
    ossp_master_json = json.load(f)
    for i in range(len(ossp_master_json["items"])): 
        if ossp_master_json["items"][i]["issue_id"] == issue_id and ossp_master_json["items"][i]["name"] == name:
            new_id = ossp_master_json["items"][i]["issue_id"]
            new_name = ossp_master_json["items"][i]["name"]
            print(new_id, new_name)
            raise AssertionError
        else:
            pass
        
        
def test_version_alpha():
    issue_id = "376"
    name = "SYCLomatic-test"
    version = "alpha"
    release_date = "Not Available"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=str(issue_id)+"\n"+name+"\n")
    assert result.exit_code == 0
    f = open(f"{osspoi}/version_details/{issue_id}-{name}-Versiondetails.json")
    data = json.load(f)
    for i in range(len(data)):
        if data[i]["version"] == version:
            test_data = data[i]
            break   
    assert test_data["version"] == version
    assert test_data["release_date"] == release_date
    