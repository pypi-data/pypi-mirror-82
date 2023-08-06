import re
import click
import os
from dulwich.repo import Repo
import urllib.request, json
from ...utils.token import parse_token

@click.command()
@click.option('--name', help='build identifer', required=True, type=str, metavar='BUILD_ID')
@click.option('--source', help='repository name and its commit hash. please specify repoName=hash pair like --source main=./main --source lib=./main/lib', default=["main=."], metavar="REPO_NAME", multiple=True)
def build(name, source):
  token, org, workspace = parse_token()

  if not all(re.match(r'[^=]+=[^=]+', s) for s in source):
      raise click.BadParameter('--source should be REPO_NAME=REPO_DIST')

  repos = [s.split('=') for s in source]
  sources = [(name, Repo(repo_dist).head().decode('ascii')) for name, repo_dist in repos]
  submodules = []
  for name, repo_dist in repos:
    # invoke git directly because dulwich's submodule feature was broken
    submodule_stdouts = os.popen("cd {};git submodule status --recursive".format(repo_dist)).read().splitlines()
    for submodule_stdout in submodule_stdouts:
      # the output is e.g. "+bbf213437a65e82dd6dda4391ecc5d598200a6ce sub1 (heads/master)"
      matched = re.search(r"^[\+\-U ](?P<hash>[a-f0-9]{40}) (?P<name>\w+)", submodule_stdout)
      if matched:
        hash = matched.group('hash')
        name = matched.group('name')        
        if hash and name:
          submodules.append((name, hash))

  # Note: currently becomes unique command args and submodules by the hash. But they can be conflict between repositories.
  uniq_submodules = {hash: (name, hash) for name, hash in sources + submodules}.values()

  try:
    commitHashes = [{
      'repositoryName': name,
      'commitHash': hash
    } for name, hash in uniq_submodules]
    print(commitHashes)

    if not (commitHashes[0]['repositoryName'] and commitHashes[0]['commitHash']):
      exit('Please specify --source as --source .')

    payload = {
      "buildNumber": name,
      "commitHashes": commitHashes
    }

    headers = {
      "Content-Type" : "application/json",
      'Authorization': 'Bearer {}'.format(token)
    }

    url = "https://api.mercury.launchableinc.com/intake/organizations/{}/workspaces/{}/builds".format(org, workspace)

    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(request) as response:
      response_body = response.read().decode("utf-8")
      print(response_body)

  except Exception as e:
    print(e)