"""Reviewed repository execution metadata; contains no task answers or test outcomes."""

from dataclasses import dataclass

PROFILES = {
    'pallets/click': ('src/click/', 'legacy-v1',
                     'sha256:6794463c9014b7ee687d70c940cf0b29ae001ba3318fa844f83b194ba35fd875'),
    'more-itertools/more-itertools': ('more_itertools/', 'method-subtests-v2',
                                    'sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad'),
}


@dataclass(frozen=True)
class RepositoryProfile:
    repo: str
    source_prefix: str
    collector_protocol: str
    image_id: str
    install_project: bool
    pids: int


def repository_profile(repo):
    if repo not in PROFILES:
        raise ValueError('Choose a reviewed repository execution profile')
    prefix, collector, image = PROFILES[repo]
    return RepositoryProfile(repo, prefix, collector, image, collector == 'legacy-v1',
                             64 if collector == 'legacy-v1' else 128)
