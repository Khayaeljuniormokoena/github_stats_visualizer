from requests import session
from pandas import DataFrame, read_csv
from datetime import datetime
from os import makedirs, path
from os.path import isdir, isfile
from shutil import rmtree
import numpy as np
import matplotlib.pyplot as plt
from my_exceptions_module import NotFoundError, ApiRateLimitError, BadCredentialsError


class Downloader:
    '''Downloader class for fetching, pre-process and caching data about a given github repository.'''
    def __init__(self,
                 owner,
                 repo,
                 token='',
                 useCacheIfAvailable=True,
                 verbose=True):
        self.__url = f'https://api.github.com/repos/{owner}/{repo}'
        self.__repo = repo
        self.__owner = owner
        self.__session = session()
        self.__cache_path = path.join('data', owner, repo)
        self.__useCache = useCacheIfAvailable
        self.__verbose = verbose

        # create cache directory if does not exists yet
        if not isdir(self.__cache_path):
            makedirs(self.__cache_path)

        # if the user provided a GitHub Oauth token then the downloader will use it in every request
        if token:
            self.__session.headers.update({'Authorization': f'token {token}'})

        # checking if the requested repository exists
        response = self.__session.get(self.__url)

        if response.ok:
            self.__log(
                f'The maximum number of requests you are permitted to make per hour: {response.headers["X-RateLimit-Limit"]}'
            )
            self.__log(
                f'The number of requests remaining in the current rate limit window: {response.headers["X-RateLimit-Remaining"]}'
            )
        else:
            self.__raise_error(response)

    def __raise_error(self, response):
        '''Raises a proper error in case of known problems or a general exception in case of unknown problem.'''

        if response.status_code == 403:
            raise ApiRateLimitError(
                'API rate limit exceeded. Try to specify an OAuth token to increase your rate limit.'
            )

        if response.status_code == 404:
            raise NotFoundError(
                f"Repository '{self.__repo}' of user '{self.__owner}' not found."
            )

        if response.status_code == 401:
            raise BadCredentialsError(
                'Bad credentials were provided for the API.')

        raise Exception(response.json()['message'])

    def __call_api(self, path, headers={}):
        response = self.__session.get(f'{self.__url}/{path}', headers=headers)

        if response.ok:
            return response.json()
        else:
            self.__raise_error(response)

    def __save_cache(self, dataFrame, file_name):
        '''Method for saving (caching) a dataframe into a given file.'''
        dataFrame.to_csv(path.join(self.__cache_path, f'{file_name}.csv'),
                         sep='\t',
                         encoding='utf-8')

    def __read_cache(self, file_name):
        '''Method for reading the cached data into a pandas dataframe.'''
        return read_csv(path.join(self.__cache_path, f'{file_name}.csv'),
                        sep='\t',
                        encoding='utf-8',
                        index_col=0)

    def __is_cache_available(self, file_name):
        '''Checks whether there is cached data available or not.'''
        return isfile(path.join(self.__cache_path, f'{file_name}.csv'))

    def __log(self, text, end='\n'):
        '''Prints out the message if the downloader is in verbose mode.'''
        if self.__verbose:
            print(text, end=end)

    def delete_cache(self):
        '''Deletes all cache of the current repository.'''
        rmtree(self.__cache_path)
        makedirs(self.__cache_path)

    def get_contributors_statistic(self):
        '''Get contributors list with additions, deletions, and commit counts.'''

        # return cached data if it is available and requested by the user
        if self.__useCache and self.__is_cache_available(
                'total_contributions') and self.__is_cache_available(
                    'weekly_contributions'):
            return self.__read_cache('total_contributions'), self.__read_cache(
                'weekly_contributions')

        data = self.__call_api('stats/contributors')

        total_contributions = []
        weekly_contributions = []

        # parsing data into dataframes
        for item in data:
            total_contributions.append({
                'commits': item['total'],
                'user': item['author']['login']
            })

            for week in item['weeks']:
                weekly_contributions.append({
                    'user':
                    item['author']['login'],
                    'week_unix_ts':
                    week['w'],
                    'date':
                    datetime.fromtimestamp(week['w']).date(),
                    'additions':
                    week['a'],
                    'deletions':
                    week['d'],
                    'commits':
                    week['c'],
                })

        total_contributions_df = DataFrame(total_contributions,
                                           columns=['user', 'commits'])
        self.__save_cache(total_contributions_df, 'total_contributions')

        weekly_contributions_df = DataFrame(weekly_contributions,
                                            columns=[
                                                'user', 'week_unix_ts', 'date',
                                                'additions', 'deletions',
                                                'commits'
                                            ])
        self.__save_cache(weekly_contributions_df,
                          'weekly_contributions')

        return total_contributions_df, weekly_contributions_df

    def get_code_frequency_statistic(self):
        '''Returns a weekly aggregate of the number of additions and deletions pushed to the repository.'''
        if self.__useCache and self.__is_cache_available('code_frequency'):
            return self.__read_cache('code_frequency')

        data = self.__call_api('stats/code_frequency')

        code_frequency = DataFrame(
            data, columns=['week_unix_ts', 'additions', 'deletions'])
        code_frequency['date'] = code_frequency.apply(
            lambda row: datetime.fromtimestamp(row.week_unix_ts).date(),
            axis=1)
        self.__save_cache(code_frequency, 'code_frequency')

        return code_frequency

    def get_issues(self):
        '''List issues in a repository.'''

        if self.__useCache and self.__is_cache_available('issues'):
            return self.__read_cache('issues')

        self.__log('Fetching repository issues ', end='')

        page = 1
        issues = []

        while (True):
            self.__log('.', end='')

            data = self.__call_api(f'issues?per_page=100&page={page}')

            if len(data) == 0:
                break

            for issue in data:
                issues.append({
                    'id':
                    issue['id'],
                    'state':
                    issue['state'],
                    'created_at':
                    datetime.strptime(issue['created_at'],
                                      '%Y-%m-%dT%H:%M:%SZ').date()
                })

            page = page + 1

        self.__log('.')

        issues_df = DataFrame(issues, columns=['id', 'state', 'created_at'])
        self.__save_cache(issues_df, 'issues')

        return issues_df

    def get_commit_activity(self):
        '''Plots a pie chart showing the top contributors based on the commit count.
        With the optional limit parameter the number of shown contributor can be modified.'''

        total_contributions, _ = self.get_contributors_statistic()

        limit = 10

        # overriding limit if it is out of bounds
        if limit > len(total_contributions.index):
            limit = len(total_contributions.index)

        if limit < 2:
            limit = 10

        # parsing data
        commits = total_contributions['commits'][-limit:].to_numpy()
        users = total_contributions['user'][-limit:].to_numpy()

        rest = sum(total_contributions['commits'][:-limit].to_numpy())

        commits = np.concatenate([[rest], commits])
        users = np.concatenate([['Others'], users])

        # commits by author - pie chart
        fig = plt.figure(figsize=self.__figsize)
        plt.pie(commits,
                labels=users,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                explode=np.full(len(commits), 0.05))

        centre_circle = plt.Circle((0, 0), 0.75, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        plt.tight_layout()
        plt.title(self.__fig_title('Commits by authors'))
        plt.show()

    def get_stargazers(self):
        '''Lists the people that have starred the repository.'''

        if self.__useCache and self.__is_cache_available('stargazers'):
            return self.__read_cache('stargazers')

        self.__log('Fetching stargazers ', end='')

        page = 1
        stargazers = []

        while (True):
            self.__log('.', end='')

            data = self.__call_api(
                f'stargazers?per_page=100&page={page}',
                {'Accept': 'application/vnd.github.v3.star+json'})

            if len(data) == 0:
                break

            for stargazer in data:
                stargazers.append({
                    'user':
                    stargazer['user']['login'],
                    'starred_at':
                    datetime.strptime(stargazer['starred_at'],
                                      '%Y-%m-%dT%H:%M:%SZ').date()
                })

            page = page + 1

        self.__log('.')

        stargazers_df = DataFrame(stargazers,
                                  columns=['user', 'starred_at'])
        self.__save_cache(stargazers_df, 'stargazers')

        return stargazers_df
