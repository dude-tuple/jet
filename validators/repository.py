from datetime import datetime
from typing import List, Optional

from pydantic import  BaseModel, HttpUrl

from .user import User


class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: HttpUrl
    description: Optional[str] = None
    fork: bool
    homepage: Optional[str] = None
    language: Optional[str] = None
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    topics: List[str] = []
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: Optional[bool] = None
    archived: bool
    disabled: bool
    visibility: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    allow_rebase_merge: Optional[bool] = None
    squash_merge_allowed: Optional[bool] = None
    allow_auto_merge: Optional[bool] = None
    delete_branch_on_merge: Optional[bool] = None
    allow_update_branch: Optional[bool] = None
    use_squash_pr_title_as_default: Optional[bool] = None
    is_template: bool
